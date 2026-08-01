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
- **I got three things wrong on the first pass** and they are logged below rather than edited
  out, per `PLAYBOOK.md` rule 13. One of them — which direction stairs load the kneecap — was
  backwards.

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

| Activity | MET (Compendium code) | Net kcal | % of a 2400 day | Weekly | lb/wk equivalent |
|---|---|---|---|---|---|
| 30-flight stair descent, 5–7 min | 3.5 (17070, *walking, descending stairs*) | ~15–21 | 0.75% | 126 (if daily) | 0.036 |
| 30 min city cycling | 4.3–6.8 (01015 *self-selected easy pace* → 01011 *to/from work, self-selected pace*) | ~110–215 | 4–9% | 360 (at 2×/wk) | 0.10 |

Both MET values are gross and include resting metabolism; the net column subtracts 1 MET, which
is the correction people routinely skip and which is worth ~37 kcal on the 30-minute ride alone.
The cycling range is wide because stop-start urban riding doesn't map cleanly onto a single
code — deliberately left wide, since the conclusion below holds across the whole range.

**Stairs: never log it, never eat it back.** Two orders of magnitude below the weekly signal.

**Cycling: also inside the noise floor at 2×/week — do not add calories back.** Note this
*differs* from `swimming.md`'s prescription to add 250–350 kcal on swim days, and the difference
is real, not an inconsistency: 2–3 swims add 500–1200 kcal/week, whereas 2 rides add ~360. The
swim rule does not transfer at this volume. It would start to apply if riding became near-daily
or substantially longer.

### The mgh framing trap

**Believed:** that descending ~90 m of stairs "costs ~15 kcal," because
mgh = 70 × 9.81 × 90 ≈ 62 kJ ≈ 15 kcal, with metabolic cost following from it at some efficiency.

**Why it breaks:** mgh is the energy the body *dissipates*, not the energy it *consumes*. Muscle
doing negative work absorbs mechanical energy; the metabolic cost of absorbing it is a separate,
empirically measured quantity that does not derive from mgh at any efficiency. The causal arrow
is inverted. mgh is an upper bound on mechanical work absorbed — a useful scale check for the
*loading* question, and not a calorie figure at all.

Per `PLAYBOOK.md` rule 3: the sum was arithmetically correct and physically meaningless.

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

**Hedge, stated rather than buried:** "legitimate aerobic dose" is a general-literature claim,
not a verified one for *this* dose in an already-fit rider. Stop-start urban riding spends real
time coasting and stopped, and the intensity distribution — not the 30-minute duration — is what
determines whether VO2max moves. The honest expectation is that it maintains and modestly
improves aerobic fitness rather than driving it, and that a rider who wants a genuine VO2max
stimulus needs sustained intensity that city traffic structurally interrupts. It remains the
best-value cardio available here regardless, because the interference and injury columns are
what actually separate it from the alternatives.

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
2. **No calorie adjustment at this volume** — unlike swimming. Revisit if it goes near-daily.
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
- **Riding frequency going near-daily**, which moves cycling above the noise floor in §2 and
  makes it a calorie-accounting question for the first time.
