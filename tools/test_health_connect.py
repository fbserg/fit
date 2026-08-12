"""End-to-end test for the Health Connect ingest, against a synthetic export.

Why this exists: the real pipeline cannot be exercised until the phone runs its first scheduled
export, and the table mapping in `health_connect.py` was derived from AOSP source rather than from
an export anyone has opened. Without this, the first night of real data would also be the first
test of the code reading it. A synthetic database built to the documented schema proves the
mapping, the upsert contract and the BIA quarantine now.

It does NOT prove the schema is right -- only that the code does what it intends against the
schema it believes in. Hand-verify against `python3 tools/health_connect.py schema` on the first
real export; that check is the one this cannot replace.

Run: python3 tools/test_health_connect.py
"""

from __future__ import annotations

import shutil
import sqlite3
import sys
import tempfile
import uuid as uuid_module
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import health_connect  # noqa: E402


# Two hours east, in seconds -- deliberately non-zero so a UTC-assuming bug cannot pass.
ZONE_OFFSET_SECONDS = 7200
SQUASH_START = datetime(2026, 8, 13, 19, 0, tzinfo=timezone(timedelta(seconds=ZONE_OFFSET_SECONDS)))


def millis(moment: datetime) -> int:
    return int(moment.timestamp() * 1000)


def build_synthetic_export(directory: Path) -> Path:
    """Write a SQLite database shaped like a Health Connect export, and zip it."""
    database_path = directory / "health_connect_export.db"
    connection = sqlite3.connect(database_path)

    connection.execute(
        "CREATE TABLE application_info_table (row_id INTEGER PRIMARY KEY, package_name TEXT, app_name TEXT)"
    )
    connection.execute(
        "INSERT INTO application_info_table VALUES (1, 'com.sec.android.app.shealth', 'Samsung Health')"
    )

    def interval_table(name: str, extra: str) -> None:
        connection.execute(
            f"CREATE TABLE {name} (row_id INTEGER PRIMARY KEY, uuid BLOB, app_info_id INTEGER, "
            f"last_modified_time INTEGER, start_time INTEGER, end_time INTEGER, "
            f"start_zone_offset INTEGER, end_zone_offset INTEGER{extra})"
        )

    def instant_table(name: str, extra: str) -> None:
        connection.execute(
            f"CREATE TABLE {name} (row_id INTEGER PRIMARY KEY, uuid BLOB, app_info_id INTEGER, "
            f"last_modified_time INTEGER, time INTEGER, zone_offset INTEGER{extra})"
        )

    interval_table("sleep_session_record_table", ", title TEXT, notes TEXT")
    interval_table("steps_record_table", ", count INTEGER")
    interval_table("exercise_session_record_table", ", exercise_type INTEGER, title TEXT, notes TEXT")
    instant_table("resting_heart_rate_record_table", ", beats_per_minute INTEGER")
    instant_table("weight_record_table", ", weight REAL")

    # The BIA tables. Present with data, exactly as a real Galaxy Watch export would have them --
    # the whole point is proving they are seen and refused, not merely absent.
    for table in health_connect.QUARANTINED_TABLES:
        column = {"body_fat_record_table": "percentage"}.get(table, "mass")
        instant_table(table, f", {column} REAL")
        connection.execute(
            f"INSERT INTO {table} (uuid, app_info_id, time, zone_offset, {column}) VALUES (?,1,?,?,?)",
            (uuid_module.uuid4().bytes, millis(SQUASH_START), ZONE_OFFSET_SECONDS, 12.3),
        )

    # Sleep: 7.5 h, the night before the squash game.
    sleep_start = SQUASH_START - timedelta(hours=20)
    connection.execute(
        "INSERT INTO sleep_session_record_table (uuid, app_info_id, start_time, end_time, "
        "start_zone_offset, end_zone_offset, title) VALUES (?,1,?,?,?,?,?)",
        (
            uuid_module.uuid4().bytes,
            millis(sleep_start),
            millis(sleep_start + timedelta(hours=7, minutes=30)),
            ZONE_OFFSET_SECONDS,
            ZONE_OFFSET_SECONDS,
            "Sleep",
        ),
    )
    connection.execute(
        "INSERT INTO steps_record_table (uuid, app_info_id, start_time, end_time, "
        "start_zone_offset, end_zone_offset, count) VALUES (?,1,?,?,?,?,?)",
        (
            uuid_module.uuid4().bytes,
            millis(SQUASH_START - timedelta(hours=12)),
            millis(SQUASH_START),
            ZONE_OFFSET_SECONDS,
            ZONE_OFFSET_SECONDS,
            8421,
        ),
    )
    connection.execute(
        "INSERT INTO resting_heart_rate_record_table (uuid, app_info_id, time, zone_offset, "
        "beats_per_minute) VALUES (?,1,?,?,?)",
        (uuid_module.uuid4().bytes, millis(SQUASH_START), ZONE_OFFSET_SECONDS, 54),
    )
    # A squash session: exercise_type 43, one hour, matching the lifter's stated Thursday game.
    connection.execute(
        "INSERT INTO exercise_session_record_table (uuid, app_info_id, start_time, end_time, "
        "start_zone_offset, end_zone_offset, exercise_type, title) VALUES (?,1,?,?,?,?,?,?)",
        (
            uuid_module.uuid4().bytes,
            millis(SQUASH_START),
            millis(SQUASH_START + timedelta(hours=1)),
            ZONE_OFFSET_SECONDS,
            ZONE_OFFSET_SECONDS,
            health_connect.SQUASH_EXERCISE_TYPE,
            "Squash",
        ),
    )

    # Heart rate samples: inside the session, plus one well outside it that must NOT be counted.
    connection.execute(
        "CREATE TABLE heart_rate_record_series_table (row_id INTEGER PRIMARY KEY, "
        "parent_key INTEGER, epoch_millis INTEGER, beats_per_minute INTEGER)"
    )
    for minute, bpm in enumerate([120, 150, 165, 140]):
        connection.execute(
            "INSERT INTO heart_rate_record_series_table (parent_key, epoch_millis, beats_per_minute) "
            "VALUES (1,?,?)",
            (millis(SQUASH_START + timedelta(minutes=minute * 10)), bpm),
        )
    connection.execute(
        "INSERT INTO heart_rate_record_series_table (parent_key, epoch_millis, beats_per_minute) "
        "VALUES (1,?,?)",
        (millis(SQUASH_START + timedelta(hours=5)), 200),
    )

    connection.commit()
    connection.close()

    export_zip = directory / "Health Connect.zip"
    with zipfile.ZipFile(export_zip, "w") as archive:
        archive.write(database_path, database_path.name)
    database_path.unlink()
    return export_zip


def read_jsonl(path: Path) -> list[dict]:
    import json

    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def run() -> None:
    workspace = Path(tempfile.mkdtemp(prefix="health-connect-test-"))
    source_dir = workspace / "OneDrive"
    source_dir.mkdir()
    output_dir = workspace / "data" / "health"

    # Redirect the ingest's output away from the real repo.
    health_connect.HEALTH_DATA_DIR = output_dir
    health_connect.RAW_ARCHIVE_DIR = output_dir / "raw"
    health_connect.REPO_ROOT = workspace

    try:
        build_synthetic_export(source_dir)

        report = health_connect.command_ingest(source_dir)

        assert report.written["sleep"] == (1, 1), report.written
        assert report.written["steps"] == (1, 1), report.written
        assert report.written["exercise_session"] == (1, 1), report.written
        assert report.written["resting_heart_rate"] == (1, 1), report.written
        assert report.written["weight"] == (0, 0), "weight table is empty but must still resolve"
        assert not report.absent, f"nothing should be absent in the fixture: {report.absent}"
        print("ok  all five record types resolved and ingested")

        assert sorted(report.quarantined_seen) == sorted(health_connect.QUARANTINED_TABLES), (
            f"the BIA tables exist in the fixture and must be reported as seen: "
            f"{report.quarantined_seen}"
        )
        for quarantined in health_connect.QUARANTINED_TABLES.values():
            assert not (output_dir / f"{quarantined}.jsonl").exists(), (
                f"{quarantined}.jsonl was written -- the BIA quarantine leaked"
            )
        print("ok  BIA tables seen, reported, and never written")

        sleep = read_jsonl(output_dir / "sleep.jsonl")[0]
        assert sleep["duration_min"] == 450.0, sleep
        assert sleep["start"].endswith("+02:00"), f"zone offset lost: {sleep['start']}"
        assert sleep["source_app"] == "com.sec.android.app.shealth", sleep
        print("ok  interval duration, zone offset and origin app survive the round trip")

        session = read_jsonl(output_dir / "exercise_session.jsonl")[0]
        assert session["exercise_name"] == "squash", session
        assert session["duration_min"] == 60.0, session
        assert session["hr_samples"] == 4, f"the out-of-range 200 bpm sample leaked in: {session}"
        assert session["hr_mean_bpm"] == 143.8, session
        assert session["hr_max_bpm"] == 165, session
        print("ok  squash session named, and HR summarised only within the session window")

        rhr = read_jsonl(output_dir / "resting_heart_rate.jsonl")[0]
        assert rhr["beats_per_minute"] == 54, rhr
        assert len(bytes.fromhex(rhr["uuid"])) == 16, f"uuid is not a hex-encoded BLOB: {rhr}"
        print("ok  instant records and hex-encoded uuids")

        # Idempotence: the export is a full snapshot, so a second run must change nothing.
        second = health_connect.command_ingest(source_dir)
        assert all(new == 0 for new, _ in second.written.values()), second.written
        assert len(read_jsonl(output_dir / "sleep.jsonl")) == 1
        print("ok  re-ingesting the same export is a no-op")

        # Staleness gate: fresh passes, backdated fails.
        assert health_connect.command_check(source_dir) == 0
        export_zip = health_connect.find_newest_export(source_dir)
        old = (datetime.now(timezone.utc) - timedelta(hours=100)).timestamp()
        import os

        os.utime(export_zip, (old, old))
        assert health_connect.command_check(source_dir) == 1, "a 100 h old export must fail check"
        print("ok  staleness gate passes fresh and fails a stopped export")

        # A database that is not a Health Connect export must fail loudly, not silently write zero.
        empty_dir = workspace / "empty"
        empty_dir.mkdir()
        stray = empty_dir / "stray.db"
        sqlite3.connect(stray).execute("CREATE TABLE unrelated (x INTEGER)")
        with zipfile.ZipFile(empty_dir / "Health Connect.zip", "w") as archive:
            archive.write(stray, stray.name)
        stray.unlink()
        try:
            health_connect.command_ingest(empty_dir)
        except health_connect.HealthConnectError as error:
            assert "sleep" in str(error), error
            print("ok  a foreign database fails loudly instead of writing nothing")
        else:
            raise AssertionError("ingesting a foreign database should have raised")

        print("\n9 checks passed")
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


if __name__ == "__main__":
    run()
