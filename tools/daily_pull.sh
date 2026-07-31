#!/bin/sh
# Daily Liftosaur pull with a macOS notification when something actually happened.
#
# Designed to run unattended from launchd (see liftosaur-api.md for setup). Three outcomes:
#   - new workout(s) pulled  -> notification with the count
#   - nothing new            -> silent (no notification fatigue)
#   - pull FAILED            -> loud notification. This matters: the session cookie expires
#     eventually, and a silently failing daily check reads as "no workouts" forever.
set -u
cd "$(dirname "$0")/.." || exit 1

notify() {
    /usr/bin/osascript -e "display notification \"$2\" with title \"$1\"" >/dev/null 2>&1
}

out=$(python3 tools/liftosaur.py snapshot 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
    notify "Fit: pull FAILED" "liftosaur.py snapshot exited $status — likely a stale session cookie. Run: python3 tools/liftosaur.py doctor"
    echo "$out"
    exit "$status"
fi

new=$(echo "$out" | sed -n 's/.*(+\([0-9]*\) new.*/\1/p')

if [ -n "$new" ] && [ "$new" -gt 0 ]; then
    sets=$(echo "$out" | sed -n 's/.*completed sets: \([0-9]*\).*/\1/p')
    notify "Fit: new workout pulled" "$new new workout(s) in data/. $sets completed sets total."
fi

echo "$out"
