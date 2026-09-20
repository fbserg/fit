"""Ingest Samsung Health data that reaches this Mac via Health Connect's nightly export.

The pipeline, end to end, with no third-party app and no API keys:

    Galaxy Watch -> Samsung Health -> Health Connect (Android 14+)
      -> scheduled nightly export, "Health Connect.zip", unencrypted SQLite
      -> OneDrive (phone)  ->  OneDrive sync  ->  this Mac  ->  here

Health Connect is Android-only and has no cloud API, so there is no way to reach this data
directly the way `liftosaur.py` reaches Liftosaur over HTTP. The scheduled export is the only
first-party automated path that exists. See `health.md` for the setup and the alternatives ruled
out.

Each export is a FULL snapshot, not a delta, so ingestion follows the same shape as the Liftosaur
pull: archive the raw artifact by date, then upsert canonical rows keyed by the Health Connect
record UUID. Re-ingesting the same zip twice is a no-op, and a missed day self-heals on the next
run because the next snapshot still contains it.

Commands:
    schema   inspect the newest export and print its tables, columns and row counts
    ingest   archive the newest export and upsert canonical rows into data/health/*.jsonl
    check    exit non-zero if the newest export is stale -- for the nightly launchd job

Table mapping was derived from AOSP `packages/modules/HealthFitness`
(service/java/com/android/server/healthconnect/storage/datatypehelpers/*RecordHelper.java),
corroborated against two independent working third-party parsers. It is still resolved by
introspection at run time rather than hardcoded, because the Health Connect database carries an
`onUpgrade` path and its column sets have changed across module releases.
"""

from __future__ import annotations

import json
import shutil
import sqlite3
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HEALTH_DATA_DIR = REPO_ROOT / "data" / "health"
RAW_ARCHIVE_DIR = HEALTH_DATA_DIR / "raw"

# Where OneDrive drops the phone's export. Overridable with `--source DIR` for a different
# cloud provider or a manual drop.
DEFAULT_EXPORT_DIR = (
    Path.home() / "Library/CloudStorage/OneDrive-Personal/HealthConnect"
)

# A nightly export that silently stops -- phone storage full, OneDrive unlinked, an Android update
# resetting the schedule -- is indistinguishable from "no data" unless something shouts. Same
# failure mode `daily_pull.sh` guards against for the expiring Liftosaur cookie.
STALE_EXPORT_HOURS = 48

# Health Connect carries these, Samsung Health writes them, and this project must NOT store them:
# they are the Galaxy Watch's wrist BIA. AGENTS.md rules that BIA absolutes are untrustworthy and
# that measurement methods are never compared across devices -- a wrist BIA is strictly worse than
# the InBody and mixing them would corrupt the scan trend. Dropped at ingest, deliberately, rather
# than filtered at analysis time where someone would eventually forget.
QUARANTINED_TABLES = {
    "body_fat_record_table": "body_fat",
    "body_water_mass_record_table": "body_water_mass",
    "lean_body_mass_record_table": "lean_body_mass",
    "bone_mass_record_table": "bone_mass",
}

# ExerciseSessionType.EXERCISE_SESSION_TYPE_SQUASH, from AOSP
# framework/java/android/health/connect/datatypes/ExerciseSessionType.java. Only the values this
# project actually reasons about are named; everything else keeps its integer and is still stored.
EXERCISE_TYPE_NAMES = {43: "squash", 79: "weightlifting", 8: "biking", 82: "swimming_pool"}
SQUASH_EXERCISE_TYPE = 43

# Columns every record table carries (RecordHelper.java). `uuid` is a BLOB and is the stable
# upsert key; `app_info_id` joins to application_info_table to identify the writing app.
UNIVERSAL_COLUMNS = ("uuid", "app_info_id", "last_modified_time")


class HealthConnectError(Exception):
    """Anything that should stop the run with a readable message rather than a traceback."""


@dataclass(frozen=True)
class RecordSource:
    """One Health Connect record type this project wants, and how to read it.

    `table_candidates` is a list because two of the table-name strings could not be read directly
    out of AOSP source (they are built from a RECORD_TYPE constant rather than written as a
    literal), so the resolver tries the plausible spellings and reports which one it found.
    """

    name: str
    table_candidates: tuple[str, ...]
    kind: str  # "instant" or "interval"
    value_columns: tuple[str, ...]
    required: bool = True


RECORD_SOURCES: tuple[RecordSource, ...] = (
    # Largest unmeasured input in the project. Total sleep time is ~80-90% valid against
    # polysomnography; the REM/deep breakdown is not, so sleep_stages_table is deliberately absent
    # from this list (health.md, "What to take, and what to refuse").
    RecordSource("sleep", ("sleep_session_record_table",), "interval", ("title", "notes")),
    # Genuine recovery/overreaching trend, and one of the things a wrist sensor measures well.
    # Optional: RHR support varies by Samsung Health and Galaxy Watch firmware, so an absent table
    # is a real-world state rather than a broken ingest.
    RecordSource(
        "resting_heart_rate",
        ("resting_heart_rate_record_table", "restingHeartRateRecordTable"),
        "instant",
        ("beats_per_minute",),
        required=False,
    ),
    # Would close the nutrition calibration loop. Only appears if entered manually or via a
    # Samsung scale, so it is optional by construction.
    RecordSource("weight", ("weight_record_table",), "instant", ("weight",), required=False),
    # NEAT proxy for the TDEE problem. Trend only -- never the device's kcal figure, which is a
    # derived number with an unaudited chain.
    RecordSource("steps", ("steps_record_table",), "interval", ("count",)),
    # The squash pass in cardio.md §9 is built on C-grade MET estimates. This is what upgrades it.
    RecordSource(
        "exercise_session",
        ("exercise_session_record_table",),
        "interval",
        ("exercise_type", "title", "notes"),
    ),
)


@dataclass
class IngestReport:
    export_zip: Path
    export_age_hours: float
    archived_to: Path
    resolved: dict[str, str] = field(default_factory=dict)
    absent: list[str] = field(default_factory=list)
    quarantined_seen: list[str] = field(default_factory=list)
    written: dict[str, tuple[int, int]] = field(default_factory=dict)  # name -> (new, total)


def find_newest_export(export_dir: Path) -> Path:
    if not export_dir.is_dir():
        raise HealthConnectError(
            f"No export directory at {export_dir}.\n"
            "Either the phone has not run its first scheduled export yet, or it is saving "
            "somewhere else. See health.md, step 3."
        )
    zips = sorted(export_dir.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not zips:
        raise HealthConnectError(
            f"{export_dir} exists but holds no .zip. Health Connect names it "
            '"Health Connect.zip" by default.'
        )
    return zips[0]


def export_age_hours(export_zip: Path) -> float:
    modified = datetime.fromtimestamp(export_zip.stat().st_mtime, tz=timezone.utc)
    return (datetime.now(timezone.utc) - modified).total_seconds() / 3600


def extract_database(export_zip: Path, into: Path) -> Path:
    """Unpack the export and return the SQLite file inside it.

    The archive layout is not contractual -- Google documents "a zip file" and nothing more --
    so this finds the database by inspecting the header rather than by trusting a filename.
    """
    with zipfile.ZipFile(export_zip) as archive:
        archive.extractall(into)

    candidates = [path for path in sorted(into.rglob("*")) if path.is_file()]
    for path in candidates:
        with path.open("rb") as handle:
            if handle.read(16) == b"SQLite format 3\x00":
                return path

    listing = "\n  ".join(str(p.relative_to(into)) for p in candidates) or "(empty)"
    raise HealthConnectError(
        f"No SQLite database inside {export_zip.name}. Contents:\n  {listing}\n"
        "If Health Connect changed its export format, this tool needs updating."
    )


def open_database(database_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def table_names(connection: sqlite3.Connection) -> set[str]:
    return {
        row["name"]
        for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }


def column_names(connection: sqlite3.Connection, table: str) -> set[str]:
    return {row["name"] for row in connection.execute(f'PRAGMA table_info("{table}")')}


def read_app_names(connection: sqlite3.Connection) -> dict[int, str]:
    """Map app_info_id -> package name, so every row records which app wrote it."""
    if "application_info_table" not in table_names(connection):
        return {}
    columns = column_names(connection, "application_info_table")
    key = "package_name" if "package_name" in columns else "app_name"
    return {
        row["row_id"]: row[key]
        for row in connection.execute(
            f'SELECT row_id, "{key}" FROM application_info_table'
        )
    }


def to_iso(epoch_millis: int | None, zone_offset_seconds: int | None) -> str | None:
    """Health Connect stores epoch millis and a separate zone offset in seconds, never a combined
    local timestamp. Recombining them here means downstream code never has to know that."""
    if epoch_millis is None:
        return None
    offset = timezone(timedelta(seconds=zone_offset_seconds or 0))
    return datetime.fromtimestamp(epoch_millis / 1000, tz=offset).isoformat()


def resolve_table(connection: sqlite3.Connection, source: RecordSource) -> str | None:
    present = table_names(connection)
    for candidate in source.table_candidates:
        if candidate in present:
            return candidate
    return None


def read_records(
    connection: sqlite3.Connection,
    source: RecordSource,
    table: str,
    app_names: dict[int, str],
) -> list[dict]:
    available = column_names(connection, table)

    time_columns = (
        ("start_time", "end_time", "start_zone_offset", "end_zone_offset")
        if source.kind == "interval"
        else ("time", "zone_offset")
    )
    wanted = [c for c in (*UNIVERSAL_COLUMNS, *time_columns, *source.value_columns) if c in available]
    if "uuid" not in wanted:
        raise HealthConnectError(
            f"{table} has no `uuid` column, so rows cannot be upserted safely. "
            f"Columns present: {', '.join(sorted(available))}. The Health Connect schema has "
            "changed and this tool needs updating."
        )

    selected = ", ".join(f'"{c}"' for c in wanted)
    records = []
    for row in connection.execute(f"SELECT {selected} FROM \"{table}\""):
        record: dict = {"record_type": source.name}
        raw_uuid = row["uuid"]
        record["uuid"] = raw_uuid.hex() if isinstance(raw_uuid, (bytes, bytearray)) else str(raw_uuid)

        if source.kind == "interval":
            start = row["start_time"] if "start_time" in wanted else None
            end = row["end_time"] if "end_time" in wanted else None
            record["start"] = to_iso(start, row["start_zone_offset"] if "start_zone_offset" in wanted else 0)
            record["end"] = to_iso(end, row["end_zone_offset"] if "end_zone_offset" in wanted else 0)
            if start is not None and end is not None:
                record["duration_min"] = round((end - start) / 60000, 1)
        else:
            record["time"] = to_iso(
                row["time"] if "time" in wanted else None,
                row["zone_offset"] if "zone_offset" in wanted else 0,
            )

        for column in source.value_columns:
            if column in wanted:
                record[column] = row[column]

        if "exercise_type" in record:
            record["exercise_name"] = EXERCISE_TYPE_NAMES.get(record["exercise_type"])

        if "app_info_id" in wanted:
            record["source_app"] = app_names.get(row["app_info_id"])

        records.append(record)
    return records


def attach_heart_rate(connection: sqlite3.Connection, sessions: list[dict]) -> None:
    """Summarise heart rate over each exercise session.

    There is no foreign key from an exercise session to heart rate rows -- Health Connect stores
    HR as a parent `heart_rate_record_table` plus a `heart_rate_record_series_table` of samples --
    so the correlation is a time-range join done here rather than in the database. This is the
    measurement that upgrades cardio.md §9's squash energy estimate from a C-grade MET lookup to
    something derived from this player.
    """
    present = table_names(connection)
    if "heart_rate_record_series_table" not in present:
        return
    columns = column_names(connection, "heart_rate_record_series_table")
    if not {"epoch_millis", "beats_per_minute"} <= columns:
        return

    for session in sessions:
        if not session.get("start") or not session.get("end"):
            continue
        start_ms = int(datetime.fromisoformat(session["start"]).timestamp() * 1000)
        end_ms = int(datetime.fromisoformat(session["end"]).timestamp() * 1000)
        row = connection.execute(
            "SELECT COUNT(*) AS samples, AVG(beats_per_minute) AS mean_bpm, "
            "MAX(beats_per_minute) AS max_bpm FROM heart_rate_record_series_table "
            "WHERE epoch_millis BETWEEN ? AND ?",
            (start_ms, end_ms),
        ).fetchone()
        if row and row["samples"]:
            session["hr_samples"] = row["samples"]
            session["hr_mean_bpm"] = round(row["mean_bpm"], 1)
            session["hr_max_bpm"] = row["max_bpm"]


def upsert_jsonl(path: Path, records: list[dict]) -> tuple[int, int]:
    """Merge records into an append-only JSONL keyed by uuid. Returns (new, total).

    Same contract as the Liftosaur results store (DECISIONS.md, "Results store: append-only
    JSONL, not SQLite"): re-ingesting an identical export changes nothing.
    """
    existing: dict[str, dict] = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                existing[row["uuid"]] = row

    before = len(existing)
    for record in records:
        existing[record["uuid"]] = record

    ordered = sorted(existing.values(), key=lambda r: (r.get("start") or r.get("time") or ""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in ordered))
    return len(existing) - before, len(existing)


def command_schema(export_dir: Path) -> None:
    export_zip = find_newest_export(export_dir)
    size_mb = export_zip.stat().st_size / 1_000_000
    print(f"export: {export_zip}  ({size_mb:.1f} MB, {export_age_hours(export_zip):.1f} h old)\n")

    workspace = Path(tempfile.mkdtemp(prefix="health-connect-"))
    try:
        database_path = extract_database(export_zip, workspace)
        print(f"database: {database_path.relative_to(workspace)}\n")

        connection = open_database(database_path)
        tables = sorted(table_names(connection))
        if not tables:
            raise HealthConnectError("The database has no tables. That should not happen.")

        print(f"{len(tables)} tables\n")
        for table in tables:
            count = connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            if count == 0:
                continue  # empty tables are noise; the schema question is about what has data
            marker = "  [QUARANTINED]" if table in QUARANTINED_TABLES else ""
            print(f"  {table}  ({count} rows){marker}")
            print(f"      {', '.join(sorted(column_names(connection, table)))}")

        print("\nmapping check:")
        for source in RECORD_SOURCES:
            resolved = resolve_table(connection, source)
            state = resolved if resolved else ("ABSENT (optional)" if not source.required else "MISSING")
            print(f"  {source.name:22} -> {state}")
        connection.close()
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def command_ingest(export_dir: Path) -> IngestReport:
    export_zip = find_newest_export(export_dir)
    age = export_age_hours(export_zip)

    workspace = Path(tempfile.mkdtemp(prefix="health-connect-"))
    try:
        database_path = extract_database(export_zip, workspace)
        connection = open_database(database_path)

        stamp = datetime.fromtimestamp(export_zip.stat().st_mtime, tz=timezone.utc)
        RAW_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        archived = RAW_ARCHIVE_DIR / f"{stamp.strftime('%Y-%m-%dT%H-%M-%SZ')}.zip"
        if not archived.exists():
            shutil.copy2(export_zip, archived)

        report = IngestReport(export_zip=export_zip, export_age_hours=age, archived_to=archived)

        present = table_names(connection)
        report.quarantined_seen = sorted(present & QUARANTINED_TABLES.keys())

        app_names = read_app_names(connection)
        found_any = False
        for source in RECORD_SOURCES:
            table = resolve_table(connection, source)
            if table is None:
                if source.required:
                    raise HealthConnectError(
                        f"Required record type {source.name!r} has no table in this export. "
                        f"Tried: {', '.join(source.table_candidates)}. Run `schema` and update "
                        "RECORD_SOURCES -- the Health Connect schema has changed."
                    )
                report.absent.append(source.name)
                continue

            found_any = True
            report.resolved[source.name] = table
            records = read_records(connection, source, table, app_names)
            if source.name == "exercise_session":
                attach_heart_rate(connection, records)
            report.written[source.name] = upsert_jsonl(
                HEALTH_DATA_DIR / f"{source.name}.jsonl", records
            )

        connection.close()
        if not found_any:
            raise HealthConnectError(
                "No wanted record type resolved to a table. This is not an empty phone -- it "
                "means the export is not the database this tool expects."
            )
        return report
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def command_check(export_dir: Path) -> int:
    """Staleness gate for the nightly job. A stopped export must not read as 'no data'."""
    export_zip = find_newest_export(export_dir)
    age = export_age_hours(export_zip)
    print(f"newest export: {export_zip.name}  ({age:.1f} h old)")
    if age > STALE_EXPORT_HOURS:
        print(
            f"error: export is {age:.0f} h old, over the {STALE_EXPORT_HOURS} h limit. The phone "
            "has stopped exporting -- check Health Connect > Backup and restore > Scheduled "
            "export, and that OneDrive is still linked.",
            file=sys.stderr,
        )
        return 1
    return 0


def print_report(report: IngestReport) -> None:
    print(f"ingest {report.export_zip.name}  ({report.export_age_hours:.1f} h old)")
    print(f"  archived:    {report.archived_to.relative_to(REPO_ROOT)}")
    for name, (new, total) in sorted(report.written.items()):
        print(f"  {name:22} {total:6} rows  (+{new} new)")
    if report.absent:
        print(f"  absent (optional):   {', '.join(report.absent)}")
    if report.quarantined_seen:
        print(f"  quarantined, dropped: {', '.join(report.quarantined_seen)}")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2

    command, rest = argv[1], argv[2:]
    export_dir = DEFAULT_EXPORT_DIR
    if "--source" in rest:
        index = rest.index("--source")
        export_dir = Path(rest[index + 1]).expanduser()

    try:
        if command == "schema":
            command_schema(export_dir)
        elif command == "ingest":
            print_report(command_ingest(export_dir))
        elif command == "check":
            return command_check(export_dir)
        else:
            raise HealthConnectError(f"Unknown command {command!r}. Known: schema, ingest, check.")
    except HealthConnectError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
