# Liftosaur — the program as executable code

`program.md` is the reasoning. This file is the same program in a form a phone can run and progress automatically.

**Source of truth:** `program.liftoscript` in this repo. Push it to the account with
`python3 tools/liftosaur.py push program.liftoscript` — see `liftosaur-api.md` for how that works.

**Live as of 2026-07-31.** v4 pushed from `program.liftoscript` to program `ahtmiiwx` and activated.
Verified server-side, not just on screen: 8 × `120s`, 16 × `75s`, 14 × `warmup: none`, the overhead
qualifier attached to Triceps Extension rather than its neighbour, `currentProgramId` = `ahtmiiwx`,
sync returned `clean`. The app opens on Day 1 with the per-set RPE splits rendering distinctly.

**Share link (current, v4):** https://www.liftosaur.com/p/11b2a78c
**Import path:** app → Choose Program → "Import from link" → paste. No account required to author or import; an account only adds cross-device sync.

Version history: `cc058146` (v1) → `14002621` (v2, shared progression + per-set RPE) →
`294fd952` (v3, `warmup: none`) → `11b2a78c` (v4, rest timers + comment placement fix).

Why Liftosaur and not Hevy: Hevy's free tier can't express a program with per-exercise progression rules, and the paid tier was ruled out. Liftosaur's whole program is one text file (Liftoscript), which means this repo can be the source of truth and the app is just a runner. Program authoring, the web editor, link import, and JSON/CSV export are all free and account-free; only the REST API and MCP server sit behind premium, which this workflow doesn't need.

## The script

Lives in `program.liftoscript`, not duplicated here — two copies drift, and the file is what the
push tool actually reads. Validated in the free web editor with zero parse errors, reloaded fresh
from the share link to confirm it wasn't an edit-mode artifact.

One week block, four days, loops automatically — finishing Day 4 wraps to Day 1 carrying all accumulated weights.

## Set arithmetic — verified against program.md

Day 1 = 19, Day 2 = 21, Day 3 = 13, Day 4 = 15. **Total 68**, matching `program.md`'s weekly table exactly. Every twice-weekly isolation lift's split is preserved: triceps 3+2, reverse fly 3+2, curl 3+2, calves 5+4, lateral raise 4+4.

## How the encoding works

**RIR → RPE.** Liftoscript speaks RPE and takes a single integer, so RIR N maps to RPE 10−N: RIR 2 = `@8`, RIR 1 = `@9`, RIR 0 = `@10`. Where `program.md` gives a range (RIR 1–2), the harder bound is used. The `+` suffix makes the app also prompt for *actual* logged RPE each set, so the log captures what happened rather than only what was prescribed.

**Per-set RIR splits are expressible.** `2x8-12 @9+, 1x8-12 @10+` parses — so the "bulk of sets at RIR 1, one finisher at RIR 0" pattern survives translation intact rather than being flattened to a single value. This matters: `program.md`'s monotony measures deliberately *reduced* RIR-0 exposure, and a uniform tag would have undone that.

**One progression line per exercise, confirmed.** Liftoscript applies a `progress:` declaration to every occurrence of that exercise across the whole program, and *errors* if you declare conflicting ones. So `progress:` appears only on each lift's first weekly appearance and the second inherits it. This is the property `program.md` requires — a weight earned on Day 1's triceps extension is the weight Day 3 starts from, not a second independent line.

**Supersets are native.** `superset: A` groups exercises into a rotation. Day 1 uses A/B, Day 2 uses C/D; Days 3 and 4 have none, by design.

## Known simplifications — read before trusting the app over the doc

Three prescriptions in `program.md` have no native Liftoscript mechanic. Each is encoded so the *set count* and therefore weekly volume is correct, with the real protocol in a `//` comment that the app surfaces as the exercise description during the workout.

| Prescription | Encoded as | What you must do manually |
|---|---|---|
| Myo-reps (calf raise, both days) | plain 5 / 4 sets | Set 1 is the activation set at RIR 3–4; the rest are 3–5-rep mini-sets off 15–20 s rest |
| Drop-sets (triceps extension, both days) | final set at `@10` | Drop the load ~20–30% and continue to failure |
| Overhead cable triceps extension | `Triceps Extension, Cable` + in-workout comment | Comment now says it; bracket-label syntax was tested and **would have severed shared progression** |

That last one is the one to actually remember. Liftosaur's library has no overhead positional variant, and the generic entry reads as a pushdown to anyone who doesn't know better. Overhead is the entire point — it loads the long head at a long muscle length, which is the stretch-bias rationale (`program.md`, stretch-bias paragraph). A pushdown is the one substitution the program's own table explicitly rules out.

## Exercise name mapping

Seven map exactly: incline DB press, reverse pec deck (`Reverse Fly, Leverage Machine`), DB lateral raise, flat DB press, lat pulldown, Bulgarian split squat, seated leg curl.

Three are substitutions forced by the library:

| program.md | Liftosaur | Why |
|---|---|---|
| Chest-supported row | Incline Row, Dumbbell | No chest-supported entry exists; prone on an incline bench is mechanically the same |
| Overhead cable triceps ext | Triceps Extension, Cable | No overhead positional variant; see the warning above |
| Hack squat *or* leg press | Leg Press, Leverage Machine | No hack-squat *machine* in the library (only barbell/Smith). `program.md` already lists leg press as the equal option |

Equipment picked where `program.md` left it open: standing DB curl → `Bicep Curl, Dumbbell` (no standing qualifier exists), standing calf raise → `Leverage Machine`, RDL → `Barbell`.

## Liftosaur's volume stats disagree with ours — expected, not a bug

Total sets agree exactly (68 = 68). Every *per-muscle* number is higher in Liftosaur:

| Muscle | program.md | Liftosaur |
|---|---|---|
| Quads | 9 | 11 |
| Hams | 9 | 11 |
| Chest | 9 | 15 |
| Back | 9 | 18 |
| Calves | 9 | 16 |
| Shoulders (side + rear) | 13 | 22 |
| Triceps | 5 | 10 |
| Biceps | 5 | 10 |

The cause is methodological, and the "days touched" column proves it: Liftosaur credits **synergists** alongside the primary target, while `program.md` counts **primary-target sets only**. Liftosaur shows back trained on 4 days though only 2 have a back exercise — RDL and split squat carry posterior-chain credit. Same for triceps and biceps at 3 days each, picking up pressing and pulling synergist credit.

**Judge volume by `program.md`'s numbers, not the app's.** The dose-response literature the 10–14 set target comes from counts direct sets per muscle; synergist-inclusive counting would put this program's shoulders at 22 sets/week, well past the point where the Pelland curve flattens, and prompt a cut that isn't warranted.

## Resolved by live testing

Everything below was verified by logging real sets in a throwaway session, not inferred.

**Shared progression across days — works.** Logged Day 1's triceps extension at top-of-range; `dp(5lb,8,12)` fired, and the Program preview then showed **both** Day 1 and Day 3 at the new weight. One progression line, confirmed.

**The overhead qualifier can't be a label.** `Triceps Extension, Cable[overhead]` is a hard parse error. The real syntax is a `label:` prefix — and its documented purpose is to split same-named exercises into *separate* progression tracks, which would have destroyed the property above. So the comment is not a workaround for lacking a better tool; it is the correct tool. Same for "standing, not seated" on the curl.

**Per-set RPE renders as distinct targets.** Sets 1–2 show `@9+` and set 3 shows `@10+` in the live workout UI, not one flattened value.

**Bulgarian split squat is correct as `4x8-12`.** It defaults to unilateral with separate `L:` and `R:` rep fields inside each set row, so four programmed sets are four sets *per leg*, matching `program.md`. Do **not** change it to `8x8-12` — that would double the real prescription. `Bicep Curl, Dumbbell` is also unilateral by default; harmless, just two rep fields per set.

## The duration gap — partly explained, partly unknown

Liftosaur estimates 95–102 min for Days 1–2 against `program.md`'s 32–38.

**Fixed:** the app auto-generated 3 warmup sets (5 reps at 30/50/80%) before *every* exercise, including lateral raises and calf raises. `warmup: none` now applies to all five isolation lifts and to every compound except the first of each day — which is exactly what `program.md` prescribes (2–4 ramping sets on the first working lift; general warm-ups add nothing). Verified in the live logging flow, not just the display: Incline Row and Bulgarian split squat now jump straight to Set 1, while Incline Bench Press and Leg Press still show their ramp. That removes 12/12/9/9 warmup sets across the four days — real gym time, whatever the app claims.

**Still unexplained:** the app's displayed estimate did not move at all after the fix — 01:35 / 01:42 / 01:00 / 01:13, identical, confirmed after save, after a full reload, and from a fresh load of the share link. A control test (gutting a day to one exercise) *did* move it, so the estimate is live; it simply ignores warmup configuration. An earlier additive model (`warmup×90s + working×180s`) reproduced 80–90% of each day's figure and was retracted once tested directly — it was curve-fitting, not mechanism. **We do not know Liftosaur's duration formula.**

**Then the rest timer — and this one moved the number.** The app defaults to 180 s between working
sets against `program.md`'s 90–120 s for compounds and 60–90 s for isolation. Liftoscript takes a
per-line timer as a bare value after the RPE token (`5x6-10 @9+ 120s`); it is per-occurrence, not a
shared per-exercise setting like `warmup:` or `progress:`, so compounds and isolation can carry
different values in the same program — which the single global setting cannot do. Applied 120 s to
all 8 compounds and 75 s to all 5 isolation lifts:

| Day | Before | After | Δ |
|---|---|---|---|
| 1 | 95 min | 68 min | −27 |
| 2 | 102 min | 81 min | −21 |
| 3 | 60 min | 44 min | −16 |
| 4 | 73 min | 60 min | −13 |

Weekly total 330 → 253 min, a 23% cut. So the estimate responds to rest intervals and is blind to
warmup configuration — the opposite of what we first assumed.

Still well above target: Day 1 is 30 min over the 38-min ceiling even after the cut. Pushing rest
lower trades against load protection and has not been decided.

**Standing Calf Raise was deliberately left at the global default.** Its myo-rep protocol
(15–20 s between mini-sets) isn't expressible as separate Liftoscript set groups — it's one flat
`5x12-15` clause with the real structure only in the comment. A uniform 75 s there would fight the
intended 15–20 s rests, so nothing was encoded rather than encoding something wrong.

**Do not treat the app's estimate as a measurement of this program.** Time an actual session instead — that is the only number that settles whether 32–38 min was realistic.

## Open

- **A stale duplicate program** (`gnwbqrgo`, the v1 script without `warmup: none`) is still in the account alongside the current one, both named "My Program". Delete one before training starts or the phone offers an ambiguous choice.
- **A phantom history record** (`historyCount: 1`, a 0-set "Ad-Hoc Workout" dated 2026-07-31) is in the account and was not logged by a real session. Delete it, or the first weekly review reads it as real training.
- **Increments on isolation lifts** (`dp(5lb)` lateral raise, `dp(10lb)` reverse fly) are coarse relative to the loads. Adjust in-app if progression stalls purely because the next jump is too big.
