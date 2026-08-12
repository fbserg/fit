"""Ingest Samsung Health data that reaches this Mac via Health Connect's nightly export.

The pipeline, end to end, with no third-party app and no API keys:

    Galaxy Watch -> Samsung Health -> Health Connect (Android 14+)
      -> scheduled nightly export, "Health Connect.zip", unencrypted SQLite
      -> OneDrive (phone app)  ->  OneDrive sync  ->  this Mac  ->  here

Health Connect is Android-only and has no cloud API, so there is no way to reach this data
directly the way `liftosaur.py` reaches Liftosaur over HTTP. The scheduled export is the only
first-party automated path that exists. See `health.md` for the setup and the alternatives ruled
out.

Each export is a FULL snapshot, not a delta, so ingestion follows the same shape as the Liftosaur
pull: archive the raw artifact by date, then upsert canonical rows keyed by record id. Re-ingesting
the same zip twice is a no-op.

Commands:
    schema   inspect the newest export and print its tables, columns and row counts
    ingest   not implemented until the schema has been seen -- run `schema` first
"""

from __future__ import annotations

import shutil
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Where OneDrive drops the phone's export. Overridable with `--source DIR` for a different
# cloud provider or a manual drop.
DEFAULT_EXPORT_DIR = (
    Path.home() / "Library/CloudStorage/OneDrive-Personal/HealthConnect"
)

# Health Connect carries these, Samsung Health writes them, and this project must NOT store them:
# they are the Galaxy Watch's wrist BIA. CLAUDE.md rules that BIA absolutes are untrustworthy and
# that measurement methods are never compared across devices -- a wrist BIA is strictly worse than
# the InBody and mixing them would corrupt the scan trend. Dropped at ingest, deliberately, rather
# than filtered at analysis time where someone would eventually forget.
QUARANTINED_RECORD_TYPES = frozenset(
    {"body_fat", "body_water_mass", "lean_body_mass", "bone_mass"}
)


class HealthConnectError(Exception):
    """Anything that should stop the run with a readable message rather than a traceback."""


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


def command_schema(export_dir: Path) -> None:
    export_zip = find_newest_export(export_dir)
    size_mb = export_zip.stat().st_size / 1_000_000
    print(f"export: {export_zip}  ({size_mb:.1f} MB)\n")

    workspace = Path(tempfile.mkdtemp(prefix="health-connect-"))
    try:
        database_path = extract_database(export_zip, workspace)
        print(f"database: {database_path.relative_to(workspace)}\n")

        connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        tables = [
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
        ]
        if not tables:
            raise HealthConnectError("The database has no tables. That should not happen.")

        print(f"{len(tables)} tables\n")
        for table in tables:
            count = connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            if count == 0:
                continue  # empty tables are noise; the schema question is about what has data
            columns = [
                row["name"] for row in connection.execute(f'PRAGMA table_info("{table}")')
            ]
            print(f"  {table}  ({count} rows)")
            print(f"      {', '.join(columns)}")
        connection.close()

        print(
            "\nNext: map the tables above onto sleep duration, resting heart rate, weight and\n"
            "steps, then implement `ingest`. Body-composition tables stay quarantined "
            f"({', '.join(sorted(QUARANTINED_RECORD_TYPES))})."
        )
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def command_ingest() -> None:
    raise HealthConnectError(
        "ingest is not implemented yet -- the Health Connect SQLite schema has not been seen.\n"
        "Run `python3 tools/health_connect.py schema` against a real export first, then the\n"
        "table mapping can be written against what is actually there instead of guessed."
    )


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
            command_ingest()
        else:
            raise HealthConnectError(f"Unknown command {command!r}. Known: schema, ingest.")
    except HealthConnectError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
