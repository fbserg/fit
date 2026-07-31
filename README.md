# fit

A first-principles training and nutrition program, derived from published dose-response
literature and one person's measured data — with every derivation, argument and retracted claim
left in the repo instead of edited out.

**This is not a program to copy.** Copying the 13 exercises, the set counts or the calorie target
transfers none of the value and inherits someone else's gym, joints, schedule and training age.
What transfers is the procedure. That's `PLAYBOOK.md`.

## Why it might be worth your time

Most fitness content gives you conclusions. This gives you the derivations, including the ones
that went wrong:

- A body-fat percentage is traced back through its instrument's regression chain until only ten
  impedance readings and a bodyweight are left as actually *measured* (`scans/scans.md`).
- A claim that BIA underreads lean men was asserted, then **retracted** when the literature turned
  out to disagree on the sign of the bias, not just its size (`abs.md`).
- A practitioner-consensus rule about scheduled deloads was overridden by an RCT that found they
  hurt strength with no hypertrophy benefit (`program.md`).
- A return-to-training ramp was cut from three weeks to one because the scan said muscle had been
  *maintained* across the supposed layoff — self-report lost to measurement (`DECISIONS.md`).
- An arm-volume figure was silently wrong until a separate adversarial audit pass caught it
  (`CONFIDENCE.md`).

`CONFIDENCE.md` ranks the whole program by how thin the evidence under each claim actually is,
weakest first. That file is the honest one — read it before trusting anything else here.

## Reading order

| If you want to… | Read |
|---|---|
| Steal the method and run it on yourself | **`PLAYBOOK.md`** — 16 rules, a traps table, a stall-diagnosis order of operations |
| Find out what the method needs from you before you start | **`INTAKE.md`** — the questions whose answers rewrite whole sections |
| Know how much to trust any given claim | **`CONFIDENCE.md`** — ranked weakest-first, with what would strengthen each |
| See what was decided and why, without re-litigating it | **`DECISIONS.md`** — ruling / why / reopens-if |
| Read the actual program | `program.md`, `exercises.md`, and `program.liftoscript` (the runnable form) |
| Understand the body-composition reasoning | `scans/scans.md`, then `abs.md` |
| Set up the same tooling | `liftosaur-api.md` |
| Not know what RIR, BIA, SMI or double progression mean | **`GLOSSARY.md`** — written for non-lifters, and it flags where this repo disagrees with common usage |

`profile.example.md` is the one file that is about a specific person. **If you fork this, copy it
to `profile.md` and fill it in** — that path is gitignored, so your own numbers stay on your
machine by default.

## The tooling

Programs live in this repo as text and are pushed to [Liftosaur](https://www.liftosaur.com) over
its own internal endpoints — no subscription, no browser automation, no clicking.

```bash
python3 tools/extract_cookie.py                     # refresh auth (the only maintenance task)
python3 tools/liftosaur.py doctor                   # check every link in the chain, name the fix
python3 tools/liftosaur.py push program.liftoscript # repo text -> your phone, verified
python3 tools/liftosaur.py snapshot                 # pull results back for analysis
python3 tools/hevy_csv.py <export.csv>              # convert a Hevy export to the same shape
```

No dependencies beyond the Python standard library and the `openssl` binary macOS ships with.
`liftosaur-api.md` documents the three endpoints with source-line references, including the traps
— a merge that replaces but never appends, a sync whose `versions` map silently gates which fields
land, and a WAF that returns 403 for an unrecognised user agent in a way that reads exactly like an
auth failure.

`doctor` is the piece worth copying: it walks cookie → permissions → auth → active program →
name collisions → parse → **does the account still match the repo**, and prints the command that
fixes whichever link is broken. That last check catches drift from editing the program in the app,
which is otherwise invisible until a weekly review quietly analyses the wrong program.

## Requirements

The tooling is **macOS + Chrome only**, and not incidentally: `extract_cookie.py` reads Chrome's
cookie store and decrypts it with a key from the macOS Keychain. Linux and Firefox both store that
key differently, so the script needs real work to port, not a flag. Everything else in the repo —
which is most of it — is prose and applies anywhere.

Python 3.9+. No pip packages.

## What's not here

Three things are deliberately absent, and their absence is not an oversight:

- **Raw training logs and bodyweight data** (`data/`) — gitignored. Derived findings that don't
  expose the underlying record, like the starting-load analysis in `history.md`, are committed.
- **The author's `profile.md` and the scan image** (`private/`) — gitignored. `scans/scans.md`
  keeps every number transcribed from that image, which is what the derivation-chain lesson
  actually needs; the printout itself adds an ID, a device serial, and exact timestamps that
  teach nothing.
- **Anything about sleep, stress, mobility, warm-up protocol, supplements, or rehab.** Not
  because they don't matter — sleep in particular plausibly outweighs several things this repo
  argues about at length. They were out of scope, and silence here is not a verdict that they're
  unimportant. Don't read the omissions as a null list; `program.md` has an explicit null list and
  these aren't on it.

## Caveats

Written for one person: male, mid-30s, lean, previously trained, no diagnosed joint or metabolic
issues, training at a busy commercial gym. `INTAKE.md` lists which of those assumptions breaks
which section when it doesn't hold for you.

Not medical advice, and no one here is a doctor, dietitian or physiotherapist. The protein ceiling
in particular is gated on an *assumed* absence of kidney issues — assumed, not cleared.

## License

MIT (`LICENSE`) — covering the prose as well as the scripts, so "take the method" is a real
permission and not just an invitation. Attribution appreciated, not required.
