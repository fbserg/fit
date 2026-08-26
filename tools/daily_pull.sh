#!/bin/sh
# Nightly data pull: Liftosaur over HTTP, plus Samsung Health via the Health Connect export.
#
# Designed to run unattended from launchd (see liftosaur-api.md for setup). The rule for every
# source here is the same: silence means "nothing new", never "the pipe broke". A silently failing
# daily job reads as "no training, no sleep, no squash" forever, which is worse than no job at all.
#
#   Liftosaur:      new workouts -> notify | nothing new -> silent | FAILED -> loud
#   Health Connect: new records  -> notify | nothing new -> silent | STALE/FAILED -> loud,
#                   except before first setup, where absence is expected and stays silent.
set -u
cd "$(dirname "$0")/.." || exit 1

notify() {
    if [ -x /usr/bin/osascript ]; then
        /usr/bin/osascript -e "display notification \"$2\" with title \"$1\"" >/dev/null 2>&1
    else
        echo "NOTIFY [$1] $2"
    fi
}

exit_status=0

# --- Liftosaur -------------------------------------------------------------------------------

out=$(python3 tools/liftosaur.py snapshot 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
    notify "Fit: Liftosaur pull FAILED" "liftosaur.py snapshot exited $status — likely a stale session cookie. Run: python3 tools/liftosaur.py doctor"
    exit_status="$status"
else
    new=$(echo "$out" | sed -n 's/.*(+\([0-9]*\) new.*/\1/p')
    if [ -n "$new" ] && [ "$new" -gt 0 ]; then
        sets=$(echo "$out" | sed -n 's/.*completed sets: \([0-9]*\).*/\1/p')
        notify "Fit: new workout pulled" "$new new workout(s) in data/. $sets completed sets total."
    fi
fi
echo "$out"

# --- Health Connect --------------------------------------------------------------------------
#
# The phone-side setup in health.md is a one-time manual step that may not have happened yet.
# Before the first export ever lands, a missing directory is the expected state and must stay
# silent — otherwise the job cries wolf every night over a known-pending task. Once even one
# export has been archived, the pipeline is live and any interruption becomes loud.

if [ -n "$(find data/health/raw -name '*.zip' -print -quit 2>/dev/null)" ]; then
    health_live=1
else
    health_live=0
fi

health_out=$(python3 tools/health_connect.py ingest 2>&1)
health_status=$?

if [ "$health_status" -ne 0 ]; then
    if [ "$health_live" -eq 1 ]; then
        notify "Fit: health sync BROKEN" "Health Connect ingest exited $health_status. The phone was exporting and has stopped. Check Health Connect > Backup and restore > Scheduled export, and that OneDrive is still linked."
        exit_status="$health_status"
    fi
    echo "$health_out"
else
    # Staleness is a separate failure from a failed ingest: OneDrive keeps serving yesterday's zip
    # quite happily, so a successful ingest of a week-old file is exactly what a stopped phone
    # export looks like.
    if ! stale_out=$(python3 tools/health_connect.py check 2>&1); then
        notify "Fit: health export STALE" "$(echo "$stale_out" | tail -n 1)"
        exit_status=1
    fi

    updated=$(echo "$health_out" | grep -c '(+[1-9]')
    if [ "$updated" -gt 0 ]; then
        notify "Fit: new health data" "$updated record type(s) updated from the phone."
    fi
    echo "$health_out"
    echo "$stale_out"
fi

exit "$exit_status"
