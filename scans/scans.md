# InBody Scan Log

Device: InBody 270 (2-frequency BIA, 20/100 kHz, 8-point electrodes).
Only weight + 10 impedance values are measured; everything else is derived:
TBW ← impedance regression; LBM = TBW / 0.732 (assumed hydration constant);
Fat = weight − LBM (residual of two big numbers); BMR = 370 + 21.6 × LBM(kg) (Katch-McArdle, verified reproduces printout exactly).
Consequence: ±3% TBW error (hydration, food, time of day) → PBF ±2 points.

CORRECTED 2026-07-27: an earlier note here claimed BIA reads lean people 2-4 points LOW vs DEXA. That is NOT supported. The direction of BIA bias in lean men is inconsistent across studies — one line of evidence has BIA OVERestimating by ~3.03 points in men under 15% DEXA-measured BF (and InBody-specific validation found fat mass overestimated, muscle mass underestimated), another has it underestimating by 3-5 points in lean athletes. BIA vs 4-compartment models: bias -3.5% to +4.4%, 95% limits of agreement spanning 15-20 points. DEXA is no rescue — it disagrees with 4C models, bias direction flips between studies, and error worsens in lean subjects. There is no reliable correction factor. True PBF here is unknowable to better than roughly 9-15%.
Trust: weight ≈ exact; PBF trend direction if Δ > ~2 points; never single-scan absolute values; never a cross-method comparison.

## 2026-07-27 18:16 (evening, fed — non-ideal conditions)
- Weight 154.2 lb (69.9 kg) | TBW 99.7 | dry lean 36.6 | fat mass 17.9
- PBF 11.6% (true value unknowable; plausible range ~9–15%) | SMM 76.5 lb | LBM 136.2 lb | BMI 22.1
- BMR 1705 (= Katch-McArdle on LBM, not measured) | SMI 8.1 kg/m²
- Segmental lean (% of ideal): L arm 7.41 lb / 101.3%, R arm 7.61 / 104.2%, trunk 58.8 / 100.8%, L leg 20.57 / 101.3%, R leg 20.90 / 102.9% — balanced, right side marginally stronger
- Impedance (Ω) 20kHz: RA 316.2, LA 326.6, TR 18.7, RL 256.4, LL 263.4; 100kHz: RA 281.9, LA 292.2, TR 15.9, RL 226.6, LL 232.8 — physically consistent
- Image: not published (see `PUBLISHING.md`) — every number above is transcribed from it.

## 2025-05-06 13:35 (from history strip on the 2026 printout)
- Weight 145.3 lb | SMM 75.2 lb | PBF 8.5% (true value unknowable, same caveat)

## Delta (14.7 months)
- +8.9 lb weight (the hard number) ≈ +0.6 lb/mo ≈ +70 kcal/day average surplus at historical intake
- PBF +3.1 points — exceeds test-retest noise, so majority-fat gain is probable; the exact fat/lean split is NOT resolvable (±3–4 lb error bars). SMM +1.3 lb nominal.

## Protocol for next scan (~Oct 2026)
Morning, fasted, empty bladder, no workout prior 12 h, no alcohol prior day. Same machine.
