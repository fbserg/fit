# Cardio and incidental activity — how to price anything that isn't lifting

Analyzed 2026-08-01, prompted by two specific questions: what is a 30-flight stair descent
worth, and what is 30 minutes of city cycling worth. The answers turned out to be less
interesting than the framework needed to get them, so the framework is the point and the two
activities are worked examples.

Closes the gap `INTAKE.md` flags for "any other regular cardio/sport" — partially. **Squash is
not covered here** and is known-regular (`CLAUDE.md`, Injuries). It is a court sport with
cutting, deceleration, and repeated wrist load on an already-injured wrist. It needs its own
pass and does not inherit these conclusions.

## Verdict up front

- **The stair descent is nutritionally invisible and physiologically near-empty.** Not harmful,
  not useful. Do it because stairs are there.
- **The bike is the real one.** ~10× the energy cost, genuine aerobic adaptation, and the lowest
  interference profile of any cardio modality available — better than swimming on this repo's
  own analysis, and with zero shoulder or wrist exposure.
- **The bounding-down-stairs habit is the only thing here with a downside**, and the downside is
  a fall on concrete, not accumulated wear.
- **Squash (§9, added 2026-08-12) is nutritionally invisible at 1×/week and does not interfere
  with the lifting program.** Its only finding that changes anything is on axis 4 and it is not
  about muscle: wear eye protection. A claim that squash needed a 48–72 h no-lower-body buffer was
  retracted in §9 — it had no source, and it had already been used to justify rebuilding the
  program.
- **Eight first-pass claims were wrong** and are logged in §7 rather than edited out, per
  `PLAYBOOK.md` rule 13. Two were outright backwards: which direction stairs load the kneecap,
  and whether traffic lights raise or lower the average cost of a city ride. Both energy costs
  were underestimated, and the bone argument was withdrawn entirely. The surviving conclusions
  are unchanged in direction, which is the only reason this document is still short.

## 1. The pricing framework — four axes, in this order

Most arguments about cardio never resolve because they conflate these.

| Axis | Question | Failure mode if skipped |
|---|---|---|
| **1. Energy** | kcal net, measured against the noise floor of the weigh-in protocol | "Earning back" calories that were never spent |
| **2. Adaptation** | What tissue adapts, at what dose, and has the dose saturated? | Assuming more of a thing keeps paying |
| **3. Interference** | Does it compete with the lifting program, and through which mechanism? | Modality-blind fear ("cardio kills gains") |
| **4. Risk** | What is the failure mode, and how bad is the worst version? | Pricing wear but not catastrophe |

The order matters. Axis 1 usually returns "irrelevant," which retires most of the argument
before it starts. Axis 4 is the one people skip, and it is the only one here that changed a
recommendation.

## 2. Axis 1 — the noise floor rule

**If an activity's contribution is below the resolution of the measurement protocol, it is not
a calorie decision.** This disposes of most incidental-activity questions permanently.

- Daily weigh-in noise is **±1–2 lb of water** — which is **3,500–7,000 kcal of apparent
  signal** on the scale.
- The protocol in `CLAUDE.md` adjusts on a **weekly average** against a **±150 kcal** step.

So anything under roughly 150 kcal/day is invisible to the control loop. More importantly: if
you do it habitually, **the weekly weight trend has already absorbed it.** Adding calories back
for a habitual activity double-counts it. This is the same trap `PLAYBOOK.md` rule 4 describes
for formulas — the measured trend is ground truth, and it does not need help.

**Use measured values, not desk-reference values, where both exist.** The Compendium is a
lookup table of estimates; for both activities here, direct measurement lands meaningfully
higher, and in the same direction. This is `PLAYBOOK.md` rule 16 applied to MET codes: grade the
number by how directly it measured the thing you're about to do.

| Activity | Desk MET (Compendium) | Measured MET | Net kcal (measured) | % of a 2400 day |
|---|---|---|---|---|
| 30-flight stair descent, 5–7 min | 3.5 (17070) | **4.9** (Teh & Aziz 2002, N=49) | **~24–33** | ~1.0–1.4% |
| 30 min city cycling | 6.8 (01011) | **7.4–8.7** (in-traffic, portable gas analyzer) | **~235–283** | ~10–12% |

MET values are gross and include resting metabolism; the net column subtracts 1 MET, the
correction people routinely skip — worth ~37 kcal on the 30-minute ride alone.

| Activity | Weekly net | lb/wk equivalent | Verdict |
|---|---|---|---|
| Stair descent, daily | ~170–234 | 0.05–0.07 | Below the noise floor. Never log it. |
| Cycling, 2×/wk | ~426–565 | 0.12–0.16 | Below the ±150 kcal/day step, but closer to the line than it looks. |
| Cycling, 5×/wk | ~1064–1413 | 0.30–0.40 | **Crosses the adjustment threshold.** Becomes a real calorie question. |

**Stairs: never log it, never eat it back.** Even at the measured value it is ~1% of a day.

**Cycling at 2×/week: still no calorie adjustment — but the margin is thinner than the first
pass suggested.** `swimming.md` prescribes +250–350 kcal on swim days because 2–3 swims add
500–1200 kcal/week. Two rides at the *measured* in-traffic intensity add **426–565 kcal/week**,
which at the top of the range is *inside* that band. So the honest ruling is not "the swim rule
doesn't transfer" — it's that cycling sits just below the trigger at 2×/week and enters it at
3×/week or higher. Averaged daily, 2×/week is 61–81 kcal/day against a ±150 kcal adjustment
step, so the weekly weigh-in still absorbs it. **Revisit the moment frequency goes past ~3/week.**

### The mgh framing trap

**Believed:** that descending ~90 m of stairs "costs ~15 kcal," because
mgh = 70 × 9.81 × 90 ≈ 62 kJ ≈ 15 kcal, with metabolic cost following from it at some efficiency.

**Why it breaks:** mgh is the energy the body *dissipates*, not the energy it *consumes*. Muscle
doing negative work absorbs mechanical energy; the metabolic cost of absorbing it is a separate,
empirically measured quantity that does not derive from mgh at any efficiency. The causal arrow
is inverted. mgh is an upper bound on mechanical work absorbed — a useful scale check for the
*loading* question, and not a calorie figure at all.

Per `PLAYBOOK.md` rule 3: the sum was arithmetically correct and physically meaningless.

**Confirmed by primary literature, and the confirmation is more interesting than the error.**
Margaria 1968 measured mechanical efficiency for negative work at **≈ −1.2 (i.e. 120%)** —
opposite in sign and magnitude to concentric work's ~25%. That is only possible because the load
does work *on* the muscle rather than the muscle on the load (Abbott, Bigland & Ritchie 1952,
the original human negative-work study, using a "push-me-pull-you" paired-ergometer design).
Metabolic cost is a mechanistically distinct process — eccentric cross-bridge cycling — not mgh
divided by an efficiency.

**And the two available methods disagree by 2–3×, which is worth stating rather than papering
over:**

| Method | Predicted net cost, 64–85 m descent |
|---|---|
| Margaria negative-work efficiency (smooth downhill walking) | **~9–12 kcal** |
| Teh & Aziz measured stair descent (4.9 METs, N=49) | **~24–33 kcal** |

Stairs cost roughly 2–3× what smooth downhill coasting predicts, and the reason is structural:
stair descent is *repeated per-step braking plus balance*, not continuous controlled falling.
Neither number is wrong; they measure different things. Since the question is about stairs, the
stair-specific measurement wins — but the gap is a real feature of the literature, not noise.

**Folklore flag: "descent costs about a third of ascent" is not well supported.** Teh & Aziz
measured descent at 4.9 METs against ascent at 9.6 — **51%**, not 33%. The ~1/3 figure traces
to a separate, smaller 1997 study. Use 40–50%.

## 3. Axis 2 — adaptation

### The stair descent buys almost nothing, but not for the reason I first gave

Descent loads quads and glutes eccentrically. Eccentric stair and downhill work has a real
literature showing strength, glucose-handling and bone benefits at low metabolic cost — but
predominantly in **untrained and elderly** populations. Against 9 weekly sets of hack squat and
Bulgarian split squat at 1–2 RIR (`program.md`), bodyweight eccentrics are sub-threshold.

**Bone — mechanism real, human dose claim withdrawn.** This was my strongest-sounding claim and
it does not survive contact with the human literature.

- **What's solid (A-tier within its model):** Rubin & Lanyon's isolated turkey ulna work shows
  4 cycles/day prevents disuse loss, ~36 cycles/day at 0.5 Hz produces the full anabolic
  response (133–143% of baseline BMC over 6 weeks), and going from 36 to **1,800** cycles adds
  *nothing*. Umemura 1997's rat jump training points the same way — 5 jumps beat sedentary
  control, 10/20/40 differ little among themselves, 100 is not meaningfully better.
- **What's genuinely useful and I under-weighted:** Robling/Turner/Burr's rest-insertion work.
  Mechanosensitivity desensitizes *within* a bout, and 4–8 h of rest between bouts roughly
  **doubles** the osteogenic response — 360 cycles split into 4×90 or 6×60 beat one continuous
  360-cycle bout. A single continuous descent is close to the worst possible way to distribute
  a given number of impacts.
- **What does not transfer (C-tier, per `PLAYBOOK.md` rule 16):** every number above comes from
  an isolated avian bone segment and *growing* rats. The human trials that actually produced
  measurable BMD change used doses an order of magnitude higher — Bassey & Ramsdale, **50
  jumps/day for 6–12 months**, +2.8% femoral neck BMD; Allison 2013, **50 hops/day, 7 days/week,
  for 12 months**, trabecular vBMD +6.4% vs +4.5% in the control leg. No human RCT shows 4–5
  impacts/day producing DXA-detectable change in an adult.

So the honest statement is: **the saturation mechanism is real in animals and directionally
informative; the practical human conclusion runs the other way.** Human bone responded to
*sustained, higher-repetition* impact loading over months. A mature skeleton with years of
walking and stair habituation is not a disused turkey ulna.

**Tendon — this one holds up, and it was the best-attacked claim.** Arampatzis' within-study
comparisons (not cross-study inference) are unusually clean:

| Protocol | Stiffness | Young's modulus | CSA |
|---|---|---|---|
| Reference: ~90% MVC, 4.5–6.5% strain, **3 s** load + 3 s rest | **+57%** | **+51%** | +4.2% |
| Long duration: **12 s** loading | +25% | +17% | +5.3% |
| **High strain rate: one-legged jumps, ~3× faster loading** | trend only (p=0.081) | **n.s. (p=0.194)** | trend only (p=0.089) |

Brief high-force loading under-performed sustained-strain loading in the same design and missed
significance on the primary outcomes. **Qualification, for honesty:** plyometric-training RCTs
*do* produce tendon adaptation — a 14-week Achilles plyometric RCT found +24% stiffness, others
report +20–54% from combined plyometric and resistance work, at ground-contact times of
150–250 ms. They get there by accumulating hundreds of reps over 8–14 weeks, and they include a
voluntary loaded push-off rather than pure passive impact. So the defensible claim is that brief
impacts are a **less efficient per-contact stimulus**, not that they don't work.

### The bike buys real aerobic adaptation

Thirty minutes of continuous-ish riding is a legitimate aerobic dose — mitochondrial density,
stroke volume, the actual VO2max and longevity currency that `swimming.md` was chasing. It
contributes **zero** hypertrophy, and should be priced as cardio only, exactly as swimming is.

**The intensity is higher than expected, and the "zone 2" label is wrong.** Directly measured
cycle commuters in real traffic (portable gas analyzer, mean 2.2–2.3 stops per commute) rode at
**65% VO2max and 78% HRmax** — which the authors put in the *bottom of the vigorous* category,
not the moderate one. That's upper-zone-2 to lower-zone-3 territory. Caveat honestly: that
sample's VO2max ran 31–39% above age-matched norms, so motivated riders may be inflating it.

**But a single 30-minute ride is not a "dose," and that framing was overstated.** The one
commuter-cycling RCT with a measured VO2max outcome (n=26, 10 weeks) used **148 ± 38 min/week,
averaging ~65 min per session** — roughly 4–5 rides a week — to produce **+10.5% VO2max**. Two
things follow. First, chronic adaptation required ten weeks of repeated long sessions; one ride
produces no measurable change by itself. Second, +10.5% is a novice-magnitude response, and
VO2max trainability falls sharply with training status — an already-fit, squash-playing subject
should expect materially less from the same stimulus.

Honest reframe: **a real but small aerobic stimulus per session, needing ~4–5×/week for ~8–10
weeks to move a measurable number, with a smaller expected effect here than the trial showed.**
It remains the best-value cardio available regardless, because interference and injury exposure
are what actually separate it from the alternatives — not its VO2max yield.

## 4. Axis 3 — interference

**Cycling is the lowest-interference cardio modality available, and this is well established.**
Wilson 2012 (21 studies, 422 effect sizes) is the source of the "cardio kills gains" scare, and
its own data localize the effect: **running** impaired strength (ES 1.76 → 1.44) and hypertrophy
(ES 1.23 → 0.85) versus lifting alone, while **cycling produced no statistically significant
interference**. Effects were also body-part specific — lower-body endurance work did not
interfere with upper-body outcomes.

This matches `swimming.md` exactly, and the reasoning chain is the same one: the leading
mechanism is eccentric muscle damage from foot-strike stretch-shortening cycles, which cycling
essentially lacks. **Flagged honestly:** the meta establishes the modality effect size, not the
mechanism. The eccentric-damage explanation is the leading hypothesis, not a proven causal
pathway.

Cycling additionally beats swimming on two axes specific to this lifter: it is lower-body, so it
does not touch the pull-dominant fatigue or shoulder-impingement pathways that made swimming
risky (`swimming.md`, sections 1–2), and it carries no meaningful wrist load beyond light
handlebar grip — relevant given the rehabbed right wrist.

**The stair descent's interference is negligible but not literally zero.** The repeated bout
effect is a *graded attenuation*, not an on/off switch: protection from a maximal eccentric bout
can persist ~6 months, from a low-intensity bout only ~3 weeks, so it decays and needs
re-triggering, and subsequent bouts still show smaller but measurable damage markers — especially
when speed, load, joint angle or fatigue state vary. A habitual daily descent is plausibly
holding a low-but-nonzero adaptation state. The right phrasing is **"attenuated well below a
hypertrophy-driving stimulus,"** not "removed."

## 5. Axis 4 — risk, and the only thing here that changes a recommendation

### Landing forces, with the arrest time actually stated

The variable nobody states is how long the landing takes, and that is what sets the force.
Impulse-momentum for 69.9 kg on a 3-step drop (0.54 m, v = 3.25 m/s, p = 228 N·s):

| Arrest time | Average GRF | Landing style |
|---|---|---|
| 50 ms | 7.6 BW | stiff, near-locked leg |
| 100 ms | 4.3 BW | quick |
| 150 ms | 3.2 BW | normal absorbing |
| 250 ms | 2.3 BW | soft, deep flex |

**Measured data says use the lower half of that table.** Niu 2014's meta-regression (26 studies)
puts two-leg peak vertical GRF at ~3–4 × BW for a 0.4–0.5 m drop; DeVita & Skelly measured
~3.2–3.3 × BW for *stiff* two-leg landings from a taller 0.59 m platform and ~2.3–2.4 × BW for
soft ones. McNitt-Gray's gymnast series spans 3.9–11 × BW, but the top of that range requires a
stiff heels-first near-locked-knee landing from far greater height. Single-leg landing (which is
what stairs are) concentrates more through one limb than these two-leg figures.

**Realistic central estimate: ~3.5–5 × BW peak**, with 6–8 × BW reserved for a genuinely
locked-knee landing. Also note that measured peak GRF arrives 40–50 ms after contact while the
full weight-acceptance phase runs 150–300 ms even when stiff — so a 0.1 s figure is
time-to-peak, not arrest duration, and the true time-averaged force is closer to 2–3 × BW.

The actionable part: **bending more is a ~3× force reduction and it is free.** Landing stiffness
is a choice, not a property of the staircase.

### The fall is the real risk, not the wear

Descending fast on stairs with turns has a failure mode that accumulated loading does not: a
missed step is not a failed rep, it is concrete. The reflexive response is a hand catch, and
that is the **rehabbed right wrist** (`CLAUDE.md`, Injuries) — the same joint already carrying
recurring squash load on the same side. Low probability per descent, but this happens daily,
and the downside is a quarter of pressing rather than a sore quad.

This is the only consideration in the document that changes a recommendation.

## 6. Prescription

**Stairs**
1. **Take them. Don't log them, don't eat them back.** Below the measurement noise floor.
2. **Bound if you enjoy bounding — but land soft, not stiff.** Bending through the landing cuts
   peak force roughly threefold at zero cost. Stiff-legged heel-first landings are the only way
   to reach the alarming end of the force table.
3. **Don't do it for your bones.** The human dosing evidence doesn't support it at this
   frequency and distribution, and a single continuous descent is the worst way to distribute
   impacts anyway (rest-insertion finding above).
4. **The canary is knee pain that persists to the next morning**, same rule as
   `program.md`'s 48 h joint-pain canary. Note this is *not* primarily a descent problem — see
   the correction log.

**Cycling**
1. **2×/week, 30–40 min is a good buy.** Real aerobic adaptation, lowest interference of any
   modality, no shoulder or wrist exposure.
2. **No calorie adjustment at 2×/week**, but this is a near thing rather than a comfortable
   one — two rides at measured intensity are 426–565 kcal/week, brushing the bottom of the band
   that triggers `swimming.md`'s +250–350 kcal rule. **At 3×/week or more, add the calories
   back.** At 5×/week it crosses the ±150 kcal/day adjustment step outright and becomes a
   genuine accounting question.
3. **Prefer it to swimming** if only one is going to happen. It buys the same cardiovascular
   currency without the shoulder-overuse pathway that `swimming.md` flags as the real swim risk,
   and without competing with rows and pulldowns.
4. **No timing restriction needed** for lower-body reasons on Days 1 and 2 (pressing/pulling).
   Keep it off Day 3 and Day 4, or ≥6 h away, since those are the leg days and residual fatigue
   is a performance question even where interference isn't.

## 7. Correction log

Per `PLAYBOOK.md` rule 13 — logged in place, labeled with what was believed and why it broke.

### "Patellofemoral load is higher on descent" — WRONG, backwards. 2026-08-01
**Believed:** ~3–3.5 × BW descending vs ~2.5 × BW ascending, and therefore "if knees ever
complain, it's descent that did it."
**Actual:** PF joint reaction force is **2.8 ± 0.5 × BW descending, 3.2 ± 0.7 × BW ascending**
(Costigan et al.). **Ascent is the higher joint load.**
**Why the error is instructive:** vertical GRF *is* higher on descent (measured 1.43–1.50 × BW),
and I read internal joint force off external GRF. They diverge by activity — ascent has a larger
knee flexion angle at contact, raising quadriceps moment-arm demand despite lower vertical GRF.
This is the same class of error as `PLAYBOOK.md` rule 1: a derived quantity treated as a
measured one.

### "The first flight or two captures the bone benefit" — WRONG by 3–5×, then withdrawn entirely. 2026-08-01
**Believed:** a ~40-impact osteogenic saturation point is reached within the first one or two
flights of a 30-flight descent.
**First error — wrong unit.** The dose variable is *landings*, not flights. Bounding 2–3 steps
at a time over 30 flights of 12–16 steps is **120–240 landings per descent**, so 40 impacts
arrives after **5–10 flights** (~17–33% of the descent), not two.
**Second, larger error — wrong species.** Even the corrected number rests on turkey and rat
models. Human trials needed ~50 impacts/day sustained for 6–12 months to move BMD. The
practical claim was withdrawn, not just renumbered. See §3.

### "30 flights ≈ 90 m" — assumed, not computed. 2026-08-01
Flights are 12–16 steps at 7–7.75″ risers = 2.13–2.84 m, so 30 of them is **64–85 m**, and mgh
is **10.5–14.0 kcal**, not 15. ~15% optimistic. Conclusion (trivial) unchanged.

### "6–8 × BW peak landing force" — upper bound presented as expected value. 2026-08-01
Measured central estimate is ~3.5–5 × BW for this drop height; 6–8 × BW requires a deliberately
stiff locked-knee landing. My "4 × BW average" was also mislabeled — it is a peak-adjacent
instantaneous value, not a time-average over the landing phase (which is 2–3 × BW).

### "Traffic lights drag the average intensity down" — BACKWARDS. 2026-08-01
**Believed:** that stop-start urban riding averages *below* steady-state riding, because lights
and coasting pull the mean down — the basis for an initial 5–7 MET estimate.
**Actual:** measured in-traffic commuting runs **7.4–8.7 METs**, *above* the Compendium's 6.8
desk value for self-paced commuting. **Mechanism:** kinetic energy dissipated into the brakes at
each stop has to be regenerated entirely on the next acceleration. Stops don't average the cost
down, they add discrete expensive events — the same principle as the measured cost of walking
speed changes. Two to three stops per commute is enough to push the average up, not down.
**Consequence:** the 30-minute ride is worth ~235–283 kcal net, not the ~170–180 first claimed.

### Both activities' energy costs were underestimated. 2026-08-01
Stairs used the Compendium's 3.5 MET desk value; direct measurement (Teh & Aziz 2002, N=49) puts
descent at **4.9 METs**, so net cost is ~24–33 kcal rather than ~15–21. Conclusion unaffected —
it is ~1% of a day either way — but the doc briefly used a desk estimate where a measurement
existed, which is the exact failure `PLAYBOOK.md` rule 16 exists to prevent. Cycling was
corrected in the same direction and by more; see the entry above.

### "The swim calorie rule doesn't transfer to cycling" — too confident. 2026-08-01
**Believed:** that 2 rides add ~360 kcal/week against swimming's 500–1200, so the +250–350 kcal
swim-day rule plainly doesn't apply.
**Actual:** at measured intensity, 2 rides add **426–565 kcal/week** — the top of that range sits
*inside* the swim band. The ruling survives at 2×/week only because the daily average
(61–81 kcal) stays under the ±150 kcal adjustment step. It fails at 3×/week. The original
statement was right by accident and for the wrong reason.

### "The repeated bout effect has removed any stimulus" — overstated. 2026-08-01
RBE is graded attenuation, not binary, and it decays (~3 weeks from a low-intensity bout).
Corrected to "attenuated well below a hypertrophy-driving stimulus." See §4.

## 8. What would change this read

- **A human RCT dosing impact loading below ~50 contacts/day** with DXA or pQCT outcomes in
  trained adults. Would reopen §3's bone conclusion in either direction — currently the entire
  practical question sits on animal models and two high-dose human trials.
- **Direct measurement of single-leg stair-bounding GRF**, which as far as I can find does not
  exist. Every number in §5 is transferred from two-leg drop-landing protocols, which is a
  known-imperfect transfer flagged rather than hidden.
- **Any wrist symptom after a stumble**, which would move the fall risk in §5 from theoretical
  to logged, and probably ends the bounding habit.
- **Riding frequency going to 3×/week or more**, which is where the calorie ruling in §2
  inverts — not "near-daily" as first written. At 5×/week it crosses the ±150 kcal/day
  adjustment step outright.
- **A second in-traffic cycling measurement** in a sample that isn't self-selected for fitness.
  The 7.4–8.7 MET figure driving §2's numbers rests on one study whose riders had VO2max 31–39%
  above age norms. It disconfirmed the initial assumption rather than confirming it, which is
  the good direction for a single study to point, but it is still a single study.
- **Direct calorimetry on bounding down stairs**, which does not exist. The energy figures in §2
  are for normal descent; the bounding case is an extrapolation, flagged as such.

## 9. Squash — the court-sport pass, run 2026-08-12

The last unanalyzed regular activity in the project. `INTAKE.md` has listed court sport as
genuinely open since 2026-08-01 and `CLAUDE.md` warns explicitly that squash does **not** inherit
the cycling verdict. It now has its own pass, on the same four axes in the same order.

**Input, from the lifter (2026-08-12):** one Thursday session per week, **~60 min booked, ~40 min
of actual play**, recreational — "we're not pros so it's not just absolutely killer."

### Axis 1 — energy

Same method as §2: net METs = gross − 1, at 69.9 kg (154 lb), so net kcal/min = (MET−1) × 1.223.

| Component | MET | Source grade | Net kcal |
|---|---|---|---|
| 40 min play, lower bound | 7.3 | Compendium 15511 "squash, general" — desk value | ~308 |
| 40 min play, upper bound | ~10 | club-level match play at ~70% VO₂max — measured, but not on this player | ~440 |
| 20 min warmup / water / chat | ~2 | assumed | ~24 |
| **Session total** | | | **~330–465 net** |

The Compendium's *other* squash entry (15510, Taylor code) is **12 METs** and would give ~540. It
is a competitive-play value and is deliberately not used — but note §7's repeated lesson that on
both prior activities the measured value came in *above* the desk value, in the same direction.
The honest read is that ~465 is a likelier miss than ~330. **Confidence: C.** Nothing here was
measured on this player; that is what the Health Connect ingest exists to fix.

| Activity | Weekly net | lb/wk equivalent | kcal/day averaged | Verdict |
|---|---|---|---|---|
| Squash, 1×/wk | ~330–465 | 0.09–0.13 | 47–66 | Below the ±150 step. No adjustment on its own. |
| Cycling, 2×/wk (§2) | ~426–565 | 0.12–0.16 | 61–81 | Below the step, closer than it looks. |
| **Squash 1× + cycling 2×** | **~756–1030** | **0.22–0.29** | **108–147** | **At the threshold. This is the real trigger.** |

**Axis 1 returns "irrelevant" for squash alone, and that retires most of the argument** — which is
exactly what this axis is for. But the *combined* tally is the finding worth keeping: squash counts
as the third non-lifting session the moment cycling starts at 2×/week, and 108–147 kcal/day sits
against a ±150 step with no margin left. §6's "revisit past ~3/week" rule fires on the tally, not
on any single activity.

**Thursday's 2300 → 2500 recode, priced honestly.** It covers ~200 kcal of a ~400 kcal cost — right
sign, roughly half the magnitude, and entirely inside the noise floor. It is **bookkeeping, not a
lever**: it exists because coding the week's highest-output day as a rest day is indefensible on its
face, not because 200 kcal will show up on the scale. Note the tension with this section's own rule
that a *habitual* activity is already absorbed by the weekly trend and does not need paying for —
that rule presumes a trend exists. There are zero weigh-ins since 2026-07-27, so nothing has been
absorbed by anything. The recode is superseded the moment the loop has data.

### Axis 2 — adaptation

One 40-minute intermittent session per week sits **below the frequency threshold for meaningful
VO₂max adaptation** (~2–3×/wk minimum). It contributes **zero hypertrophy** — no progressive
overload, no sustained tension at length, same verdict `swimming.md` reached by the same reasoning.

This is not a criticism. The dose has not saturated; it was never an adaptation dose. Squash is
recreation, and it should be priced as recreation and not defended as training.

### Axis 3 — interference

**Negligible, and this axis was previously answered wrongly in conversation.** Concurrent-training
interference scales with endurance frequency and duration and is modality-graded (eccentric/impact
work interferes; cycling and swimming do not). One 40-min intermittent session per week is at the
bottom of every published dose-response, and hypertrophy is the outcome *least* affected by
concurrent training — strength and power are hit harder.

**Retracted here, in place:** a claim made 2026-08-12 that squash required a **48–72 h no-lower-body
window on both sides**, which was load-bearing for a proposed rebuild of all four training
templates. It had no source in this repo or in the literature — the only systematic review of
racket-sport physiological demands found no squash studies at all and reports no muscle-damage
marker for any racket sport. The nearest measurement runs the other way: a 3-hour simulated tennis
match dropped 1RM squat 35% immediately post-match with strength and jump height **not significantly
different from baseline at 24 h**, described by the authors as mild muscle damage. This lifter is
additionally protected twice over — the repeated-bout effect never lapses at weekly intervals, and
resistance-trained men already carry the adaptation. The full ruling and what it cost is in
`DECISIONS.md`, "The squash restructure is refused."

Practical consequence: **lifting legs the day after squash is fine**, and lifting them the day
before is a squash-*performance* preference, not injury prevention.

### Axis 4 — risk, which is again the only axis that changes anything

| Risk | Severity | Read |
|---|---|---|
| **Eye** | **Catastrophic, cheap to eliminate** | A squash ball is ~40 mm and fits *inside* the adult orbital rim, so the bone that protects you from most projectiles does not protect you from this one. Racquet strikes add to it. Protective eyewear is the single highest-value object in the sport and most recreational players don't wear it. **This is the one actionable item on this page.** |
| **Right wrist** | Moderate, already tracked | Recurring same-side load on the rehabbed wrist, already named in `CLAUDE.md`. Green at 42.5 lb DB pressing + regular squash as of 2026-08-10. The settled schedule helps by accident: only one pressing day is adjacent to Thursday, and the day *after* is Lower B — all-machine, the lightest wrist day in the program. |
| **Achilles** | Low probability, high consequence | Racquet sports are over-represented in Achilles rupture among 30–50-year-old recreational males; the mechanism is explosive push-off out of a lunge. Interaction worth naming and **not** acting on: Wednesday's calf myo-reps run to true failure the day before Thursday. That is mechanism reasoning with nothing measured behind it — precisely the tier of claim that produced the retraction in Axis 3 above, so it is logged as a canary, not a rule. The free option already exists if it ever matters: calf raise is already Upper B's designated time-ceiling drop slot. |
| **Ankle / knee** | Ordinary | Standard court-sport cutting risk. Strength training reduces acute sports injury rates substantially (Lauersen 2014, 25 RCTs, 26,610 subjects), so the lifting program is protective here, not additive. |

### Prescription

1. **Keep playing. Change nothing about the training program for it.** Axis 1 says it's invisible,
   axis 3 says it doesn't interfere, axis 2 says it was never training.
2. **Buy eye protection.** Highest expected-value action in this entire document.
3. **Thursday eats as a 2500 day.** Bookkeeping, not a lever — see Axis 1.
4. **Watch the tally, not the activity.** Squash + cycling 2×/wk = 108–147 kcal/day, at the ±150
   threshold. Adding a third weekly ride is where calories come back.
5. **Measure it.** Duration and HR via the Health Connect ingest, 3–4 sessions, plus a Friday
   next-morning soreness check (quad / calf / hamstring, 0–10). That converts every C-grade number
   above into a measured one, and it directly tests the only live question left: whether Friday's
   Lower B rep quality actually differs from Monday/Tuesday lower work. Four Fridays settles it
   better than any literature can.
