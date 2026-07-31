#!/usr/bin/env python3
"""Push programs to, and pull training data from, a Liftosaur account over plain HTTP.

No browser, no premium subscription. Authenticates with the account's `session` cookie.
The endpoint contracts and their source references are documented in ../liftosaur-api.md.

Usage:
    python3 tools/liftosaur.py doctor                     # check everything, name the fix
    python3 tools/liftosaur.py status
    python3 tools/liftosaur.py snapshot                   # pull results into data/ (idempotent)
    python3 tools/liftosaur.py pull                      # full storage JSON to stdout
    python3 tools/liftosaur.py push program.liftoscript  # replace the active program's content
    python3 tools/liftosaur.py push-share 11b2a78c       # import from a /p/<hash> share link
    python3 tools/liftosaur.py activate <programId>

Auth: put the `session` cookie value in `.liftosaur-session` (gitignored) or the
LIFTOSAUR_SESSION environment variable. The cookie is httpOnly, so it has to be read
out of the browser's cookie store, not from page JavaScript.

Everything here fails loudly. A stale session, a moved endpoint, or a schema rejection
raises — it never returns an empty result that a weekly review would misread as
"no changes this week".
"""

from __future__ import annotations

import base64
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_BASE = "https://api3.liftosaur.com/api"
REPO_ROOT = Path(__file__).resolve().parent.parent
SESSION_FILE = REPO_ROOT / ".liftosaur-session"

# Identifies our writes in the account's event log, so a human reading Liftosaur's
# own history can tell which changes came from this repo rather than from the app.
DEVICE_ID = "fit-repo"

# The API sits behind a WAF that 403s unrecognised user agents, before it ever looks at
# the cookie. Without this every call fails with a misleading "forbidden".
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


class LiftosaurError(RuntimeError):
    """Any failure talking to Liftosaur. Never swallowed, never defaulted around."""


def read_session_cookie() -> str:
    from_env = os.environ.get("LIFTOSAUR_SESSION", "").strip()
    if from_env:
        return from_env
    if SESSION_FILE.exists():
        from_file = SESSION_FILE.read_text(encoding="utf-8").strip()
        if from_file:
            return from_file
    raise LiftosaurError(
        f"No session cookie. Write the `session` cookie value to {SESSION_FILE} "
        f"or set LIFTOSAUR_SESSION. See liftosaur-api.md for how to get it."
    )


def request_json(
    path_or_url: str,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    authenticated: bool = True,
) -> Any:
    url = path_or_url if path_or_url.startswith("http") else f"{API_BASE}{path_or_url}"
    encoded_body = json.dumps(body).encode("utf-8") if body is not None else None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": BROWSER_USER_AGENT,
    }
    if authenticated:
        headers["Cookie"] = f"session={read_session_cookie()}"

    request = urllib.request.Request(url, data=encoded_body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        if error.code == 401:
            raise LiftosaurError(
                f"401 from {method} {url}. The session cookie is expired or wrong.\n"
                f"Fix: python3 tools/extract_cookie.py\n"
                f"Server said: {detail}"
            ) from error
        if error.code == 403:
            raise LiftosaurError(
                f"403 from {method} {url}. This is the WAF, not authentication — the "
                f"User-Agent header is missing or has been blocklisted. Server said: {detail}"
            ) from error
        raise LiftosaurError(f"{error.code} from {method} {url}: {detail}") from error


def fetch_storage() -> dict[str, Any]:
    """The account's complete IStorage: settings, programs, history, stats."""
    payload = request_json("/storage")
    storage = payload.get("storage")
    if not isinstance(storage, dict):
        raise LiftosaurError(
            f"/storage returned no `storage` object. Endpoint may have moved. Got keys: {list(payload)}"
        )
    for required_field in ("version", "programs", "settings"):
        if required_field not in storage:
            raise LiftosaurError(f"/storage response is missing `{required_field}` — schema changed.")
    return storage


def fetch_shared_program(share_hash: str) -> dict[str, Any]:
    """Decode a /p/<hash> share link into the IExportedProgram envelope it wraps.

    The payload is doubly encoded: base64 of a `data:` URI whose own base64 body is gzipped JSON.
    """
    payload = request_json(f"/p/{share_hash}", authenticated=False)
    if "data" not in payload:
        raise LiftosaurError(f"/p/{share_hash} returned no `data` field. Got keys: {list(payload)}")

    data_uri = base64.b64decode(payload["data"]).decode("utf-8")
    if "," not in data_uri:
        raise LiftosaurError(f"/p/{share_hash} payload is not a data: URI — encoding changed.")
    exported = json.loads(gzip.decompress(base64.b64decode(data_uri.split(",", 1)[1])))

    if "program" not in exported:
        raise LiftosaurError(f"Decoded share payload has no `program`. Got keys: {list(exported)}")
    return exported


def parse_liftoscript_into_weeks(script_text: str) -> list[dict[str, Any]]:
    """Split a Liftoscript file on `# Week N` / `## Day N` headers into planner weeks.

    Returns [{"name": "Week 1", "days": [{"name": "Day 1", "exerciseText": "..."}]}].
    """
    weeks: list[dict[str, Any]] = []
    current_day_lines: list[str] = []

    def flush_day() -> None:
        if weeks and weeks[-1]["days"]:
            weeks[-1]["days"][-1]["exerciseText"] = "\n".join(current_day_lines).strip() + "\n"

    for line in script_text.splitlines():
        week_header = re.match(r"^#\s+(.*\S)\s*$", line)
        day_header = re.match(r"^##\s+(.*\S)\s*$", line)
        if day_header:
            flush_day()
            current_day_lines = []
            if not weeks:
                raise LiftosaurError("Found a `## Day` header before any `# Week` header.")
            weeks[-1]["days"].append({"name": day_header.group(1), "exerciseText": ""})
        elif week_header:
            flush_day()
            current_day_lines = []
            weeks.append({"name": week_header.group(1), "days": []})
        else:
            current_day_lines.append(line)
    flush_day()

    if not weeks:
        raise LiftosaurError("No `# Week` headers found — this does not look like a Liftoscript program.")
    for week in weeks:
        if not week["days"]:
            raise LiftosaurError(f"Week {week['name']!r} has no `## Day` sections.")
        for day in week["days"]:
            if not day["exerciseText"].strip():
                raise LiftosaurError(f"Day {day['name']!r} in {week['name']!r} has no exercises.")
    return weeks


def build_exported_program(storage: dict[str, Any], program: dict[str, Any]) -> dict[str, Any]:
    """Wrap an IProgram in the IExportedProgram envelope POST /api/program requires.

    `version` is the account's STORAGE SCHEMA version and must match the server exactly,
    or the write is rejected with 400 "Version mismatch". It is a sibling of `program`,
    not a field inside it — IProgram has no version field at all.
    """
    return {
        "program": program,
        "customExercises": storage["settings"].get("exercises", {}),
        "version": storage["version"],
        "settings": storage["settings"],
    }


def resolve_target_program(storage: dict[str, Any], program_id: str | None) -> dict[str, Any]:
    """Pick which existing program to overwrite.

    POST /api/program upserts by id using a plain `.map()`, so it can only REPLACE a program
    that already exists — it will not append a new one. We therefore always target an
    existing program object, which also guarantees a schema-conformant result.
    """
    programs = storage["programs"]
    if not programs:
        raise LiftosaurError(
            "The account has no programs. Import one once through the web UI "
            "(liftosaur.com/p/<hash> -> 'Add this program to your account'), then this tool can update it."
        )
    if program_id:
        for program in programs:
            if program["id"] == program_id:
                return program
        available = ", ".join(f"{p['id']} ({p['name']})" for p in programs)
        raise LiftosaurError(f"No program with id {program_id!r}. Available: {available}")

    current_id = storage.get("currentProgramId")
    for program in programs:
        if program["id"] == current_id:
            return program
    if len(programs) > 1:
        available = ", ".join(f"{p['id']} ({p['name']})" for p in programs)
        raise LiftosaurError(
            f"No active program set and {len(programs)} to choose from — pass --program-id. Available: {available}"
        )
    return programs[0]


def save_program(storage: dict[str, Any], program: dict[str, Any], source: str) -> str:
    response = request_json(
        "/program",
        method="POST",
        body={
            "program": build_exported_program(storage, program),
            "deviceId": DEVICE_ID,
            "source": source,
        },
    )
    saved_id = response.get("data", {}).get("id")
    if not saved_id:
        raise LiftosaurError(f"POST /program did not return an id: {response}")
    return saved_id


def set_current_program(program_id: str) -> dict[str, Any]:
    """Make a program the active one.

    POST /api/program never touches currentProgramId, so this needs a sync. The merge is
    per-field last-write-wins: a field absent from `versions` is IGNORED no matter what
    `storage` contains, so both halves must name the field.
    """
    storage = fetch_storage()
    if not any(program["id"] == program_id for program in storage["programs"]):
        raise LiftosaurError(f"Program {program_id!r} is not in the account — save it before activating it.")

    now_ms = int(time.time() * 1000)
    response = request_json(
        "/sync2",
        method="POST",
        body={
            "storageUpdate": {
                "version": storage["version"],
                "originalId": storage.get("originalId"),
                "versions": {"currentProgramId": now_ms},
                "storage": {"currentProgramId": program_id},
            },
            "deviceId": DEVICE_ID,
            "timestamp": now_ms,
            "historylimit": 20,
        },
    )
    if response.get("type") == "error":
        raise LiftosaurError(f"sync2 rejected the update: {response.get('error')}")

    confirmed = fetch_storage().get("currentProgramId")
    if confirmed != program_id:
        raise LiftosaurError(
            f"sync2 reported success but currentProgramId is still {confirmed!r}, not {program_id!r}."
        )
    return response


def verify_program_landed(program_id: str, expected_marker: str) -> None:
    """Read back after writing. A write that reports success but did not land is the
    failure mode most likely to go unnoticed, so we always check."""
    program = next((p for p in fetch_storage()["programs"] if p["id"] == program_id), None)
    if program is None:
        raise LiftosaurError(f"Program {program_id!r} vanished after the write.")
    if expected_marker not in json.dumps(program):
        raise LiftosaurError(
            f"Program {program_id!r} saved, but the expected content {expected_marker!r} is not in it. "
            f"The write did not take."
        )


DATA_DIR = REPO_ROOT / "data" / "liftosaur"
RAW_DIR = DATA_DIR / "raw"
HISTORY_FILE = DATA_DIR / "history.jsonl"
COMPLETED_SETS_FILE = DATA_DIR / "completed_sets.jsonl"


def weight_to_lb(weight: Any) -> float | None:
    """Liftosaur weights are {value, unit}. Normalise to pounds so analysis never mixes units."""
    if not isinstance(weight, dict) or "value" not in weight:
        return None
    value, unit = weight["value"], weight.get("unit", "lb")
    if unit == "lb":
        return float(value)
    if unit == "kg":
        return round(float(value) * 2.2046226218, 2)
    raise LiftosaurError(f"Unknown weight unit {unit!r} — refusing to guess.")


def flatten_completed_sets(record: dict[str, Any]) -> list[dict[str, Any]]:
    """One row per set that was ACTUALLY PERFORMED.

    This exists to make the most dangerous mistake in this codebase impossible. Every set carries
    both what was planned (`reps`, `weight`, `rpe`) and what was done (`completedReps`,
    `completedWeight`, `completedRpe`), gated by `isCompleted`. Reading the planned fields yields
    numbers that look like results and are not — silently breaking stall detection, progression
    health, volume adherence and completion rate all at once. Analysis reads this file, not the
    raw records.
    """
    rows = []
    for entry in record.get("entries", []):
        exercise = entry.get("exercise") or {}
        exercise_name = f"{exercise.get('id', '?')}, {exercise.get('equipment', '?')}"
        for set_index, performed_set in enumerate(entry.get("sets", [])):
            if not performed_set.get("isCompleted"):
                continue
            rows.append(
                {
                    "workout_id": record["id"],
                    "date": record.get("date"),
                    "start_time": record.get("startTime"),
                    "program_name": record.get("programName"),
                    "day_name": record.get("dayName"),
                    "week": record.get("week"),
                    "day_in_week": record.get("dayInWeek"),
                    "exercise": exercise_name,
                    "exercise_id": exercise.get("id"),
                    "equipment": exercise.get("equipment"),
                    "set_index": set_index,
                    "planned_reps": performed_set.get("reps"),
                    "reps": performed_set.get("completedReps"),
                    "reps_left": performed_set.get("completedRepsLeft"),
                    "weight_lb": weight_to_lb(performed_set.get("completedWeight")),
                    "rpe": performed_set.get("completedRpe"),
                    "is_amrap": performed_set.get("isAmrap", False),
                    "is_unilateral": performed_set.get("isUnilateral", False),
                }
            )
    return rows


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def command_snapshot() -> None:
    """Pull results and fold them into the local store. Idempotent: safe to run any number of times.

    Three artifacts, all gitignored — this repo is public and training logs are not:
      raw/<utc>.json      every response verbatim, append-only, never rewritten
      history.jsonl       canonical workout records, upserted by `id`, tombstones applied
      completed_sets.jsonl  flattened performed sets — what the analysis actually reads
    """
    storage = fetch_storage()
    stamp = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime())

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / f"{stamp}.json"
    raw_path.write_text(json.dumps(storage, indent=2), encoding="utf-8")

    incoming = storage.get("history", [])
    if not isinstance(incoming, list):
        raise LiftosaurError(f"storage.history is {type(incoming).__name__}, expected list — schema changed.")

    # `progress` is the in-flight, unfinished workout. Counting it would inject a phantom
    # half-session into every check, so it is excluded by construction.
    in_flight = storage.get("progress")
    in_flight_ids = {p["id"] for p in in_flight if isinstance(p, dict) and "id" in p} if isinstance(in_flight, list) else set()

    existing = {record["id"]: record for record in read_jsonl(HISTORY_FILE)}
    before = len(existing)
    added = updated = 0
    for record in incoming:
        if "id" not in record:
            raise LiftosaurError(f"History record without an `id`: {json.dumps(record)[:200]}")
        if record["id"] in in_flight_ids:
            continue
        if record["id"] in existing:
            if existing[record["id"]] != record:
                updated += 1
        else:
            added += 1
        existing[record["id"]] = record

    # A workout deleted in the app must not resurrect locally on the next pull.
    tombstones = storage.get("deletedHistory") or []
    removed = sum(1 for tombstone_id in tombstones if existing.pop(tombstone_id, None) is not None)

    records = sorted(existing.values(), key=lambda record: record.get("startTime", 0))
    write_jsonl(HISTORY_FILE, records)
    write_jsonl(COMPLETED_SETS_FILE, [row for record in records for row in flatten_completed_sets(record)])

    completed_sets = sum(1 for _ in read_jsonl(COMPLETED_SETS_FILE))
    print(f"snapshot {stamp}")
    print(f"  raw:            {raw_path.relative_to(REPO_ROOT)}")
    print(f"  workouts:       {before} -> {len(records)}  (+{added} new, {updated} changed, -{removed} deleted)")
    print(f"  completed sets: {completed_sets}")
    if in_flight_ids:
        print(f"  skipped {len(in_flight_ids)} in-flight workout(s) — not finished, not counted")
    if not records:
        print("  (no workouts logged yet — this is expected until you train)")


def command_doctor() -> int:
    """Check every link in the chain and name the exact fix for whichever one is broken.

    Run this first whenever anything looks wrong, and before any scheduled job that
    assumes the account is reachable.
    """
    failures = 0

    def check(label: str, ok: bool, detail: str, fix: str = "") -> None:
        nonlocal failures
        print(f"  [{'ok' if ok else 'FAIL'}] {label}: {detail}")
        if not ok:
            failures += 1
            if fix:
                print(f"         fix: {fix}")

    print("liftosaur doctor")

    cookie_present = SESSION_FILE.exists() or bool(os.environ.get("LIFTOSAUR_SESSION"))
    check(
        "session cookie",
        cookie_present,
        f"{SESSION_FILE.name} present" if SESSION_FILE.exists() else
        ("LIFTOSAUR_SESSION set" if cookie_present else "missing"),
        "python3 tools/extract_cookie.py",
    )
    if SESSION_FILE.exists():
        mode = SESSION_FILE.stat().st_mode & 0o777
        check("cookie permissions", mode == 0o600, f"mode {mode:o}", f"chmod 600 {SESSION_FILE}")
    if not cookie_present:
        return 1

    try:
        storage = fetch_storage()
    except LiftosaurError as error:
        check("api auth", False, str(error).splitlines()[0], "python3 tools/extract_cookie.py")
        return 1
    check("api auth", True, f"authenticated as {storage.get('email', '<unknown>')}")

    active_id = storage.get("currentProgramId")
    active = next((p for p in storage["programs"] if p["id"] == active_id), None)
    check(
        "active program",
        active is not None,
        f"{active_id} ({active['name']!r})" if active else f"{active_id!r} is not a real program",
        "python3 tools/liftosaur.py activate <programId>",
    )

    duplicate_names = len(storage["programs"]) != len({p["name"] for p in storage["programs"]})
    check(
        "no duplicate program names",
        not duplicate_names,
        f"{len(storage['programs'])} program(s)"
        + (" — same-named programs are ambiguous on the phone" if duplicate_names else ""),
    )

    script_path = REPO_ROOT / "program.liftoscript"
    if not script_path.exists():
        check("repo program", False, "program.liftoscript not found", "")
        return 1
    try:
        weeks = parse_liftoscript_into_weeks(script_path.read_text(encoding="utf-8"))
    except LiftosaurError as error:
        check("repo program parses", False, str(error), "")
        return 1
    total_days = sum(len(week["days"]) for week in weeks)
    check("repo program parses", True, f"{len(weeks)} week(s), {total_days} day(s)")

    if active is not None:
        repo_text = [day["exerciseText"].strip() for week in weeks for day in week["days"]]
        account_text = [
            day["exerciseText"].strip()
            for week in active.get("planner", {}).get("weeks", [])
            for day in week["days"]
        ]
        in_sync = repo_text == account_text
        check(
            "account matches repo",
            in_sync,
            "identical" if in_sync else "the account has drifted from program.liftoscript",
            "python3 tools/liftosaur.py push program.liftoscript",
        )

    print(f"\n{'all checks passed' if failures == 0 else f'{failures} problem(s) found'}")
    return 0 if failures == 0 else 1


def command_status() -> None:
    storage = fetch_storage()
    current_id = storage.get("currentProgramId")
    print(f"account:  {storage.get('email', '<unknown>')}")
    print(f"version:  {storage['version']}")
    print(f"active:   {current_id}")
    print(f"history:  {len(storage.get('history', []))} records")
    print("programs:")
    for program in storage["programs"]:
        marker = "*" if program["id"] == current_id else " "
        weeks = len(program.get("planner", {}).get("weeks", []))
        days = sum(len(week["days"]) for week in program.get("planner", {}).get("weeks", []))
        print(f"  {marker} {program['id']}  {program['name']!r}  {weeks} week(s), {days} day(s)")


def command_pull() -> None:
    json.dump(fetch_storage(), sys.stdout, indent=2)
    sys.stdout.write("\n")


def command_push(script_path: str, program_id: str | None) -> None:
    script_text = Path(script_path).read_text(encoding="utf-8")
    weeks = parse_liftoscript_into_weeks(script_text)

    storage = fetch_storage()
    program = json.loads(json.dumps(resolve_target_program(storage, program_id)))
    planner = program.get("planner")
    if not planner:
        raise LiftosaurError(f"Program {program['id']!r} has no planner — it predates Liftoscript.")

    planner["weeks"] = weeks
    program["isMultiweek"] = len(weeks) > 1

    saved_id = save_program(storage, program, source="fit-repo-push")
    first_exercise_line = weeks[0]["days"][0]["exerciseText"].strip().splitlines()[0]
    verify_program_landed(saved_id, first_exercise_line)

    total_days = sum(len(week["days"]) for week in weeks)
    print(f"pushed {script_path} -> {saved_id} ({len(weeks)} week(s), {total_days} day(s)), verified")


def command_push_share(share_hash: str, program_id: str | None) -> None:
    exported = fetch_shared_program(share_hash)
    storage = fetch_storage()
    target = resolve_target_program(storage, program_id)

    # Keep the account's own id and clonedAt: `id` is what currentProgramId points at, and
    # `clonedAt` is the key the sync collection-merge uses for programs. Taking the share
    # link's values instead would orphan the program from the account's own bookkeeping.
    program = json.loads(json.dumps(exported["program"]))
    program["id"] = target["id"]
    program["clonedAt"] = target.get("clonedAt")

    saved_id = save_program(storage, program, source="fit-repo-push-share")
    first_day = program["planner"]["weeks"][0]["days"][0]["exerciseText"].strip().splitlines()[0]
    verify_program_landed(saved_id, first_day)
    print(f"pushed share /p/{share_hash} -> {saved_id}, verified")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2

    command, rest = argv[1], argv[2:]
    program_id = None
    if "--program-id" in rest:
        index = rest.index("--program-id")
        program_id = rest[index + 1]
        rest = rest[:index] + rest[index + 2 :]

    try:
        if command == "doctor":
            return command_doctor()
        elif command == "snapshot":
            command_snapshot()
        elif command == "status":
            command_status()
        elif command == "pull":
            command_pull()
        elif command == "push":
            if not rest:
                raise LiftosaurError("push needs a path to a .liftoscript file")
            command_push(rest[0], program_id)
        elif command == "push-share":
            if not rest:
                raise LiftosaurError("push-share needs a share hash, e.g. 11b2a78c")
            command_push_share(rest[0], program_id)
        elif command == "activate":
            if not rest:
                raise LiftosaurError("activate needs a program id")
            set_current_program(rest[0])
            print(f"active program is now {rest[0]}")
        else:
            raise LiftosaurError(f"Unknown command {command!r}. See --help.")
    except LiftosaurError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
