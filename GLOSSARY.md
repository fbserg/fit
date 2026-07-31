# Glossary

Written for someone who is not already a lifter. Every term below is used somewhere in this repo
without being defined at the point of use — `RIR` alone appears 94 times across 10 files.

Where the repo takes a position that differs from common usage, that's marked **⚠**. Those are the
entries worth reading even if you know the vocabulary.

## Effort and proximity to failure

**Failure** — the point in a set where you cannot complete another rep with good form. Note the
qualifier; grinding out a rep with collapsing form is past failure, not at it.

**RIR — Reps In Reserve.** How many more reps you could have done. RIR 2 means you stopped with two
left. It's the primary effort dial in this repo: nearly every set is prescribed at 1–2 RIR.

**RPE — Rate of Perceived Exertion.** The same idea on a 1–10 scale, where RPE 10 = failure, so
RPE 8 ≈ 2 RIR. This repo thinks in RIR and writes RPE only because Liftoscript's syntax uses `@`
for RPE. **⚠** Both are self-reported estimates, and novices systematically underestimate how close
to failure they are — treat early-block RIR numbers as noisy.

**AMRAP** — As Many Reps As Possible; a set taken to failure deliberately.

## Volume, load and progression

**Set / rep** — a rep is one execution; a set is a group of reps done without stopping.

**Volume** — usually "number of hard sets per muscle per week" in this repo, which is the unit the
dose-response literature uses. **⚠** Other sources mean tonnage (sets × reps × weight) by the same
word, and apps often count a set for every muscle involved rather than the one being trained. Those
three conventions can differ by 2× for the same session, which is why `PLAYBOOK.md` rule 12 says to
decide in writing which one is authoritative.

**Progressive overload** — the requirement that the demand increases over time. Without it, a
calorie surplus adds fat rather than muscle, which is the failure the baseline in this repo
documents.

**Double progression** — the specific scheme used here. Each lift has a rep range (say 6–10). You
add reps at a fixed weight until you hit the top of the range on *every* set, then add the smallest
load increment and drop back to the bottom. Two variables, one at a time.

**`dp(2.5lb, 6, 10)`** — how Liftoscript writes exactly that: increment, range bottom, range top.

**1RM** — the most you could lift once. **e1RM** is an estimate of it from a submaximal set. **⚠**
Every such formula is a curve fit that degrades badly above ~10 reps; useful for comparing a lift
to itself over time, not as a real number.

**Deload** — a deliberately easy week. **⚠** This repo autoregulates deloads off measured
performance regression and explicitly rejects putting them on a fixed calendar, on the basis of an
RCT where the scheduled version hurt strength and helped nothing (`program.md`).

**Ramp** — easing back into training after time off. Here it's one week, because the scan said
muscle had been retained; the RDL keeps three as the one high-consequence exception.

## Set structures

**Superset** — two exercises alternated with no rest between them, to save time. Used here for
non-competing muscles so the stimulus isn't compromised.

**Drop set** — reach failure, immediately cut the weight ~20–30%, keep going.

**Myo-reps** — one hard activation set, then several very short rest-pause mini-sets. A way to
accumulate near-failure reps cheaply in time.

**Warm-up set** — submaximal preparatory work. Doesn't count toward volume targets.

## Body composition and measurement

**BIA — Bioelectrical Impedance Analysis.** Passing a small current through the body and inferring
composition from resistance. What InBody and most smart scales use.

**DEXA** — X-ray absorptiometry, often treated as the reference standard. **⚠** This repo argues it
isn't one: it disagrees with 4-compartment models, and its bias direction flips between studies
(`abs.md`).

**PBF** — percent body fat. **LBM** — lean body mass (everything that isn't fat). **TBW** — total
body water. **SMM** — skeletal muscle mass. **SMI** — skeletal muscle index, SMM normalized to
height², so it's comparable between people of different sizes.

**⚠ The critical point about all of these**: on a BIA device only bodyweight and the raw impedance
readings are *measured*. Everything else — fat percentage, lean mass, BMR — is regression output
computed from them. `scans/scans.md` traces the whole chain. A ±3% error in the water estimate
moves the headline body-fat number by ±2 points.

**Skinfold** — caliper thickness at a fixed site, in mm. Cruder-sounding but a *direct* measurement,
which is why `abs.md` prefers tracking it over any device-derived percentage.

## Energy and nutrition

**BMR** — Basal Metabolic Rate, energy at complete rest. **TDEE** — Total Daily Energy Expenditure,
everything including movement and digestion. **⚠** No formula knows your TDEE to better than about
±300 kcal; this repo treats every calculated figure as a seed to be corrected against measured
weight trend.

**Katch-McArdle / Mifflin-St Jeor** — two BMR equations. The first needs lean mass and is preferred
when you have a scan; the second runs off bodyweight alone.

**NEAT** — Non-Exercise Activity Thermogenesis: fidgeting, walking, everything that isn't a workout.
Large and highly variable between people. **TEF** — Thermic Effect of Food, the energy spent
digesting. Both are routinely undercounted in handwritten TDEE math.

**MPS** — Muscle Protein Synthesis, the building process protein intake feeds. **⚠** Per-meal MPS
saturates around 0.4–0.5 g/kg, which is where the "30 g absorption cap" myth comes from — the
excess is used more slowly, not wasted.

**Surplus / deficit** — eating above or below maintenance. **Recomp** — gaining muscle and losing
fat simultaneously; realistic mainly for novices, the detrained, and people carrying more fat.

## Evidence vocabulary

**RCT** — Randomized Controlled Trial. **Meta-analysis** pools several studies; a
**meta-regression** additionally models a dose-response *curve* across them, which is what makes
Pelland 2024/25 the backbone of this repo's volume targets.

**Dose-response curve** — how outcome changes as you increase the dose. The useful feature is where
it *plateaus*; `PLAYBOOK.md` rule 5 says to set targets at the plateau rather than from a
memorized rule of thumb.

**Effect size / Cohen's d** — how big a difference is, in standard deviations, independent of
sample size. Roughly: 0.2 small, 0.5 moderate, 0.8 large.

**Confidence interval** — the range the true value plausibly sits in. **⚠** A tight interval
straddling zero is real evidence of *no effect*; a wide one straddling zero just means nobody
knows. This repo's "rep range doesn't matter" claim rests on the first kind.

**Delphi consensus** — structured expert survey. Ranks below an RCT here, and lost on the deload
question.

## Tooling

**Liftosaur** — the app the program runs in. **Liftoscript** — its text DSL, so a program is a
file in this repo rather than a thing tapped into a phone. `program.liftoscript` is the source of
truth; `tools/liftosaur.py push` sends it to the account.
