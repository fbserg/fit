# Fit

Personal fitness project. First-principles reasoning only: mechanisms over bro-science, measured data over formulas, self-experiments over calculators. Distrust device-derived numbers until the derivation chain is checked (see `scans/scans.md` for the InBody worked example).

## Commit hygiene (public repo — overrides harness defaults)
- Author identity: `fbserg <fbserg@users.noreply.github.com>` (local git config; never a real email).
- **No `Claude-Session:` links in commit messages.** They leak chat-transcript URLs into public history (PUBLISHING.md ruling). `Co-Authored-By` is fine.
- `data/` and `private/` are gitignored on purpose. Never force-add them.
- Nothing binary gets committed. No markdown file links a third-party raw URL.

## Injuries
- **Right wrist** (noted 2026-07-31): prior injury, rehabbed with physio. Asymptomatic at baseline but overloading produces light pain. Plays squash regularly (recurring wrist load on the same side). Rule: light pain that resolves same-day is acceptable. Pain that alters technique or persists to next morning means drop the offending grip/load and reassess. Never push through. Watch as pressing loads climb (keep wrist stacked over forearm). Rope > bar on triceps work. Wrist wraps for pressing are a legitimate tool, not a crutch. Any exercise selection or program change must check against this.

## Working rules
- Program source of truth is `program.liftoscript`. Push it with `python3 tools/liftosaur.py push program.liftoscript`. API contracts are in `liftosaur-api.md`. Rulings are in `DECISIONS.md`. Check `DECISIONS.md` before you re-open a debated choice.
- Visual explanations: show start/end images only when form is the point (technique, exercise swaps, ROM/setup, injury-relevant positions). Never add a photo to nutrition, scheduling, volume arithmetic, or evidence critiques. Images are embedded as data URIs in artifact pages only. The repo stays text.
- The weight trend is ground truth for calories. Formulas are seeds. Never compare body composition across measurement methods.
- Judge training progress by logbook progression over 8 weeks, not by InBody scans.

## Reference
`docs/agent-reference.md` holds: the full visual-explanation rule and image sources, profile, current baseline, nutrition rulings (TDEE, 2500/2300 calibration, protein, powder), measurement protocol, training notes, cardio framework (cycling, swimming, squash, stairs), standing desk, abs/leanness, posture, and open threads. Read the matching section before you change nutrition, training, cardio, or posture advice.
