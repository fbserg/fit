#!/usr/bin/env python3
"""Convert a Hevy CSV export into this repo's flattened set store.

Hevy is where the training history before 2026-02 lives. Its web export
(hevy.com -> Settings -> Export Data -> Export Workout Data) produces one CSV row per set.
This turns that into the same JSONL shape `liftosaur.py snapshot` writes, so analysis reads
one format across both eras instead of special-casing the past.

    python3 tools/hevy_csv.py data/hevy/workouts-2026-07-31.csv

Writes `data/hevy/hevy_sets.jsonl` and `data/hevy/hevy_workouts.jsonl`. Both are gitignored.

Two facts about the export that matter and are not obvious:

- **The `rpe` column exists but is empty** in this account's export — Hevy only records RPE if you
  enter it per set, and it was never entered. So there is no RIR/RPE signal in the history at all.
  `loop.md`'s stall checks are RIR-based and cannot run against it. This history is a load and
  volume baseline, nothing more. The column is carried through anyway so the emptiness stays
  visible rather than being silently dropped.
- **`weight_lbs` is blank for bodyweight and machine-cardio movements** (dips, planks, leg raises,
  rowing). Those rows are kept with `weight_lb: None` rather than coerced to zero — a zero would
  read as a real load in any volume calculation.

Workouts are identified by `start_time`, which is what Liftosaur's own Hevy importer uses for
duplicate detection (`src/utils/importFromHevy.ts`).
"""

from __future__ import annotations

import csv
import datetime
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "data" / "hevy"
SETS_FILE = OUTPUT_DIR / "hevy_sets.jsonl"
WORKOUTS_FILE = OUTPUT_DIR / "hevy_workouts.jsonl"

# Hevy renders timestamps in the exporting browser's locale, e.g. "Feb 3, 2026, 2:12 PM".
HEVY_TIME_FORMATS = ("%b %d, %Y, %I:%M %p", "%d %b %Y, %H:%M", "%Y-%m-%d %H:%M:%S")

# Every column Liftosaur's importer expects, plus `rpe` and `superset_id` which it ignores.
EXPECTED_COLUMNS = {
    "title", "start_time", "end_time", "exercise_title",
    "set_index", "set_type", "reps",
}


class ConversionError(RuntimeError):
    """The CSV is not the shape we know how to read. Never guess at a fix."""


def parse_hevy_time(raw: str) -> datetime.datetime:
    for time_format in HEVY_TIME_FORMATS:
        try:
            return datetime.datetime.strptime(raw, time_format)
        except ValueError:
            continue
    raise ConversionError(
        f"Unrecognised Hevy timestamp {raw!r}. Hevy formats these in the exporting browser's "
        f"locale; add the format to HEVY_TIME_FORMATS."
    )


def optional_float(raw: str) -> float | None:
    """Blank means 'no load recorded', which is not the same as zero load."""
    raw = raw.strip()
    return float(raw) if raw else None


def optional_int(raw: str) -> int | None:
    raw = raw.strip()
    return int(float(raw)) if raw else None


def workout_id(start_time: str) -> str:
    """Stable id derived from start time — the same key Liftosaur dedupes Hevy imports on."""
    return "hevy-" + hashlib.sha256(start_time.encode("utf-8")).hexdigest()[:12]


def read_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ConversionError(f"{csv_path} has no data rows.")
    missing = EXPECTED_COLUMNS - set(rows[0].keys())
    if missing:
        raise ConversionError(
            f"{csv_path} is missing expected column(s): {sorted(missing)}. "
            f"Hevy changed its export format; this script needs updating."
        )
    return rows


def convert(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    set_rows: list[dict[str, Any]] = []
    workouts: dict[str, dict[str, Any]] = {}

    for row in rows:
        start_raw = row["start_time"]
        started = parse_hevy_time(start_raw)
        identifier = workout_id(start_raw)

        if identifier not in workouts:
            ended = parse_hevy_time(row["end_time"]) if row.get("end_time", "").strip() else None
            workouts[identifier] = {
                "workout_id": identifier,
                "source": "hevy",
                "date": started.date().isoformat(),
                "start_time": int(started.timestamp() * 1000),
                "end_time": int(ended.timestamp() * 1000) if ended else None,
                "duration_min": round((ended - started).total_seconds() / 60, 1) if ended else None,
                "day_name": row.get("title", "").strip() or None,
                "notes": row.get("description", "").strip() or None,
                "set_count": 0,
            }
        workouts[identifier]["set_count"] += 1

        set_rows.append(
            {
                "workout_id": identifier,
                "source": "hevy",
                "date": started.date().isoformat(),
                "start_time": int(started.timestamp() * 1000),
                "program_name": None,  # Hevy has routines, but the export does not name them
                "day_name": row.get("title", "").strip() or None,
                "exercise": row["exercise_title"],
                "exercise_id": row["exercise_title"],
                "equipment": None,  # baked into the Hevy name, e.g. "Bench Press (Barbell)"
                "set_index": optional_int(row["set_index"]),
                "set_type": row["set_type"],
                "is_warmup": row["set_type"] == "warmup",
                "planned_reps": None,  # Hevy exports performed sets only; there is no plan to compare
                "reps": optional_int(row["reps"]),
                "weight_lb": optional_float(row.get("weight_lbs", "")),
                "rpe": optional_float(row.get("rpe", "")),  # empty in practice — see the module docstring
                "distance_km": optional_float(row.get("distance_km", "")),
                "duration_seconds": optional_int(row.get("duration_seconds", "")),
                "notes": row.get("exercise_notes", "").strip() or None,
                "superset_id": row.get("superset_id", "").strip() or None,
            }
        )

    set_rows.sort(key=lambda item: (item["start_time"], item["exercise"], item["set_index"] or 0))
    workout_rows = sorted(workouts.values(), key=lambda item: item["start_time"])
    return set_rows, workout_rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().split("\n\n")[0], file=sys.stderr)
        print(f"\nusage: python3 {Path(argv[0]).name} <hevy-export.csv>", file=sys.stderr)
        return 2

    try:
        rows = read_rows(Path(argv[1]))
        set_rows, workout_rows = convert(rows)
    except ConversionError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    write_jsonl(SETS_FILE, set_rows)
    write_jsonl(WORKOUTS_FILE, workout_rows)

    working = [row for row in set_rows if not row["is_warmup"]]
    with_rpe = [row for row in set_rows if row["rpe"] is not None]
    print(f"wrote {SETS_FILE.relative_to(REPO_ROOT)}: {len(set_rows)} sets ({len(working)} working)")
    print(f"wrote {WORKOUTS_FILE.relative_to(REPO_ROOT)}: {len(workout_rows)} workouts "
          f"({workout_rows[0]['date']} -> {workout_rows[-1]['date']})")
    if not with_rpe:
        print("note: 0 sets carry an RPE — this history cannot feed loop.md's RIR-based stall checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
