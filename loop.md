# The weekly review loop

Design for a recurring process: pull logged sets from Liftosaur, check them against
`program.md`'s own documented rules, write a dated report, propose a diff. No silent edits.

## 1. Prior art verdict

Asked twice, checked exhaustively across five independent sweeps (fitness-specific,
autoregulation-specific, quantified-self, Liftosaur/Hevy-ecosystem-specific, and a critic
pass hunting the term of art). Answer holds every time: **the exact closed loop does not
exist as a usable open-source artifact.** Nobody publishes a repo that (a) pulls a lifting
log on a schedule, (b) grades it against a user-authored, citation-backed rule document,
(c) writes recommendations, (d) occasionally edits the program file, (e) pushes the result
back into the app. That specific chain is a genuine gap, not a blind spot in the search.

What *does* exist, and what to take from each:

| Artifact | Stars / status | Covers | Verdict |
|---|---|---|---|
| RP Hypertrophy App, JuggernautAI, Alpha Progression, Boostcamp | Paid, shipped, active 2026 | The full loop, for real | **Commercial proof the pattern works.** Closed-source, own logger, no external ruleset, no Liftosaur hook. Proves the category is a business model, not a gift-wrapped repo. |
| watt-mind/coach | 75★, pushed 2026-07-31 | Scheduled pull → analysis → adaptive plan, for endurance (power/HRV/CTL-ATL-TSB) | Proves the *architecture* is viable and being built today by someone else — wrong domain (no sets/reps/RIR concept), would need a rewrite not a fork. |
| BorisBW/claude-fitness-cn ("Coach Paddy") | 16★, pushed 2026-06-12 | Reads accumulated strength-log volume over weeks, can update a plan | Closest domain match. **Manual-invocation only** — no cron. Missing exactly the automation half. |
| Liftosaur first-party MCP server | Part of 641★ main repo, MCP shipped ~5 months ago | Read/write API for programs, history, stats | The right plumbing, but **premium-gated** (already ruled out, `liftosaur.md`) and its own issue tracker shows write endpoints erroring (#554) and OAuth tokens expiring hourly with no refresh (#560) as of 2026-07-31. Chat-triggered only regardless — no scheduling primitive of its own. |
| lucasnp1/hevy-ai-coach + four near-identical zero-star clones | 0★ each, all built in the last ~5 months | Scheduled (daily) pull → LLM → chat feedback, on Hevy not Liftosaur | A cluster of hobbyists independently reinventing this right now, none hardened, none starred, none cross-pollinating. Evidence the gap is real and actively felt, not evidence it's solved. |
| LiftShift | 478★, pushed within 24h | Real plateau-detection algorithm (session-since-progress, static vs general plateau) against Hevy/Strong/Lyfta/CSV | The one genuinely good piece of stall-detection code found anywhere. **Does not support Liftosaur**, is manual-refresh in-browser, never writes anywhere. Worth reading the algorithm shape, not adoptable directly. |
| karlicoss/HPI | 1618★, pushed 2026-07-22 | Cron-pull-and-normalize architecture for dozens of personal data sources | Steal the *pattern* (cache raw JSON separately from derived state, idempotent sync) — do not adopt the 130-module framework itself, overkill for one feed. |
| rbrands/intervals-icu-sync | 12★, pushed 2026-07-24 | Pull → rule-based summary → human pastes into ChatGPT/Claude → human pastes plan back | Structurally the same shape as this design, one week old, for cycling. Every step is manual copy-paste, not automated end to end. |

**Bottom line to give the user:** no, this doesn't exist on GitHub as something to clone.
Yes, you're right to be skeptical that the *idea* is novel — paid apps sell exactly this
loop, and at least six different hobbyist teams (Hevy-coach clones, Coach Paddy, coach,
intervals-icu-sync) are independently building pieces of it in 2026. What's missing in
every case is the specific combination this repo needs: free tier, checked against a
hand-authored evidence-cited rule document rather than a black-box heuristic, and running
on a schedule without a human relaying JSON between two chat windows. Build it; don't wait.

## 2. The data path

Liftosaur premium (needed for the REST API / MCP server) is off the table per
`liftosaur.md`. Two free mechanisms exist. **The authenticated endpoint is the chosen
one**; the public profile page is recorded below as the rejected alternative.

### Chosen: the app's own storage endpoint

`GET https://api3.liftosaur.com/api/storage`, cookie-authenticated.

Discovered by watching what the app itself calls on load (`POST /api/sync2` on the same
host gave away the API domain). Verified live in a signed-in session: **200, ~12 KB, the
complete `storage` object** — `settings`, `programs`, `history`, `stats`, `subscription` —
plus `email` and `user_id` at the top level. The same shape the premium REST API would
serve, without the premium gate.

- **Nothing is published.** The account stays private. This is the decisive advantage over
  the profile page, which serves the same data to anyone including search crawlers.
- **Auth is an httpOnly cookie.** Not readable from page JavaScript (only `lft_landing` is
  JS-visible), so a scheduled job needs the cookie extracted from Chrome's cookie store
  once and stored locally. That is a real, if small, secret to manage: it is a session
  credential for the account, and it belongs in a gitignored file, never in a commit.
- **Failure mode: session expiry.** When the cookie dies the pull returns 401/403 and the
  loop must fail LOUDLY — a report saying "could not fetch, re-auth needed" — never a
  silent skip or an empty report that reads like "no changes this week". Re-auth is a
  manual sign-in, so this is the one recurring human action, and it should be rare.
- **Second failure mode: undocumented endpoint.** This is not an API contract; Liftosaur
  can change or remove it. The parser must validate against the `IStorage` shape and fail
  loudly on mismatch rather than returning partial data.

### Rejected: the public profile page

`https://www.liftosaur.com/profile/<userId>` — toggle "Is Profile Page Public?" and the
server renders the entire `IStorage` into a `<div id="data">` as escaped JSON, fetchable
by plain `curl` with no auth at all. Genuinely zero-effort, and it works.

Rejected because the same dump carries `email` and a subscription receipt, the page has no
`noindex`, and `robots.txt` permits crawling — real users' profiles are already indexed by
Google. The URL is unguessable, not access-controlled. The user accepted the email
exposure ("email is fine whatever"), so this stayed viable on their terms, but the
authenticated endpoint delivers identical data while publishing nothing, which makes the
tradeoff unnecessary rather than merely acceptable. Keep as the fallback if the endpoint
disappears.

## 3. What the weekly review actually checks

Each check's rule is copied from `program.md`/`AGENTS.md` verbatim in spirit — nothing
here is invented.

| # | Check | Input needed | Rule (source) | Action triggered |
|---|---|---|---|---|
| 1 | **Stall detection** | Per-exercise set/rep/weight history, last 2 sessions of that lift | "no scheduled deloads... reps drop at the same load across two sessions" (`program.md`, Deloads) | Flag the lift. If joints/sleep also degrading, recommend the deload protocol (1 wk, ~half volume, same exercises, +3 RIR). |
| 2 | **Double progression health** | Per-exercise reps-at-top-of-range vs weight trend over 3–4 sessions | "Hit top of rep range for all sets → add smallest load increment, drop to bottom" (`program.md`, Progression) | If a lift has sat at the *bottom* of its rep range for 3+ consecutive logged sessions without reps climbing, flag as stalled progression (distinct from check 1 — this is "not advancing," not "regressing"). No auto-action; report only. |
| 3 | **Volume adherence** | Completed sets per exercise this week, mapped to primary-target muscle only (per `liftosaur.md`'s explicit ruling: ignore the app's synergist-inclusive numbers) | Weekly table: quads 9, hams 9, chest 9, back 9, calves 9, side delts 8, rear delts 5, triceps 5, biceps 5 (`program.md`) | Report actual vs target per muscle. Systematic shortfall (2+ consecutive weeks under target on the same muscle) → flag for review, not auto-correct. |
| 4 | **Completion rate / session count** | Sessions logged vs 4 scheduled that week; sets completed vs sets prescribed per session | "adherence — the third growth variable... completion rate × weeks sustained" (`program.md`; `exercises.md` ranks it growth variable #2) | Report the number. This is the metric the program's own break-even argument for the free-choice/monotony-measure design assumes exists — it must be measured, not asserted. |
| 5 | **Session duration** | Wall-clock time per logged session (Liftosaur timestamps first-set to last-set) | Target 32–38 min per day, ceiling ~45 min (`program.md`, Estimated length + Time ceiling) | If duration is consistently over ~45 min, flag — check whether the built-in time-ceiling rule (drop last isolation slot) is actually being applied, before proposing anything structural. |
| 6 | **Weight-trend calorie rule** | Daily weigh-ins (external to Liftosaur — separate input), weekly average | ">0.5 lb/wk gain → −150 kcal, flat → +150" (`AGENTS.md`, Nutrition rulings) | Compute the weekly average trend, apply the rule, report the suggested calorie delta. This is a nutrition-side check riding along in the same report, not a Liftosaur-derived one. |

## 4. What may and may not be changed automatically

`program.md` and `exercises.md` establish an explicit hierarchy: weekly sets, RIR, and
progressive overload carry the entire measured hypertrophy effect size and are the reason
this program looks the way it does. Exercise selection within a slot is nearly free
(dose-response literature shows most swaps are growth-equivalent — that's the entire
premise of the program's own "fixed substitutions" table). Exercise churn is separately
and actively harmful: `program.md`'s Progression section states untracked/frequently-swapped
lifts cannot be progressively overloaded, and mandates keeping lifts 6–12+ weeks. The loop
must encode this asymmetry structurally, not rely on remembering it in the moment.

| | Free variables — loop may propose these directly | Load-bearing variables — loop must never silently change |
|---|---|---|
| **What's in this bucket** | Which pre-approved substitute is used on a given day; free-choice slot picks (lateral raise DB/cable, curl standing/incline); rest-period discipline notes; flagging that the time-ceiling or minimum-viable-session rule should have been invoked; noting a completion-rate or duration problem | Weekly sets per muscle; RIR/proximity-to-failure targets; the double-progression rule itself; which of the 13 fixed exercises occupies a slot; the ramp schedule; the deload trigger threshold |
| **Why** | These are the variables `program.md` itself already declares interchangeable/near-zero-cost (stretch-bias-equivalent subs, RCT-proven growth-equivalent free choices) | These are the five effect-size-ranked variables the whole program is built to maximize (`program.md` §1) — a convenience-driven change here silently erases the thing the evidence sweep was for |
| **Loop behavior** | May write directly into the weekly report as a suggestion, and may propose the corresponding Liftoscript diff | May only ever *flag* (e.g. "check 1 fired: RDL stalled 2 sessions running") and cite the existing rule that already tells the user what to do — never emit an edited number, never touch `program.md`'s exercise list or `liftosaur.md`'s script for these fields without an explicit approved diff the user reads and applies themselves |
| **Exercise substitution specifically** | Recommending a swap is rare, evidence-triggered only (e.g. a documented pain/joint-comfort issue, not "variety"), and must say explicitly which of `program.md`'s pre-vetted subs it invokes — never a novel exercise, never a default weekly output | — |

The loop is a **read-and-report tool with a proposed-diff step**, never a write-to-`program.md`
tool. `program.md`/`liftosaur.md`/`exercises.md`/`AGENTS.md` are edited by hand after the
user reads the report — consistent with `PLAYBOOK.md` rule 13 (log corrections in place,
labeled, never silently).

## 5. Mechanism

Smallest thing that works for a single-user local-first repo (`AGENTS.md`: no hypothetical
abstractions). No new service, no database, no framework.

```
weekly cron (launchd on macOS, or Claude Code's native /schedule / CronCreate)
        │
        ▼
curl the public profile URL → extract div#data → unescape → json.parse
        │  (validate against IStorage/IHistoryRecord shape; fail loudly, not silently, on mismatch)
        ▼
save raw pull to  scans/liftosaur-pulls/YYYY-MM-DD.json   (raw, never overwritten — HPI's
        │                                                   raw/derived separation)
        ▼
run the 6 checks in §3 against program.md's own stated numbers (read fresh each run,
never hardcoded — the rules can change and the checker must not drift from them)
        │
        ▼
write   reviews/YYYY-MM-DD-weekly-review.md    — dated report, human-readable, checks
        │                                          1–6 each get: input observed / rule /
        │                                          verdict / recommended action or "no
        │                                          action, still within range"
        ▼
if a free-variable change is warranted: also emit a proposed diff (program.md /
liftosaur.md snippet) inline in the same report — NOT applied to the file
        │
        ▼
user reads the dated report, applies the diff by hand (or asks the assistant to apply it
in a normal editing session), commits normally
```

Directory layout to add (not created by this task — design only):
- `scans/liftosaur-pulls/` — raw JSON, one file per pull, append-only.
- `reviews/` — one markdown report per week, append-only, never edited after the fact
  (matches `PLAYBOOK.md` rule 13: corrections get a new dated entry, not a silent rewrite).

No new repo, no hosted service, no webhook. A weekly `/schedule`-triggered Claude Code
session (or a plain cron job invoking `claude -p` with a fixed prompt) is enough — this is
exactly the "native scheduling primitive, nobody has wired it to a lifting log" gap
identified in §1.

## 6. What would make this fail

Stated honestly, because the loop is worthless if it manufactures signal that isn't there.

- **4 sessions/week means a weekly window is 4 data points.** Noise dominates early. A
  single missed rep or a single bad-sleep session can look like check 1's stall trigger
  when it's just variance. The checker should require the *rule's own* threshold (two
  consecutive sessions at the same load, not one) before flagging — already encoded in §3,
  but worth restating: do not lower that bar to make the report feel more active.
- **Ramp weeks (program.md's 3-week return-to-training ramp) produce progression data by
  design that looks like nothing is stalling** — RIR 4→3→2 across weeks 1–3 means every
  session should show rising performance almost automatically, and the double-progression
  checker (check 2) will see false "healthy" signal. The loop should suppress checks 1–2
  entirely during the documented ramp window and say so explicitly in the report ("ramp
  week 2 of 3 — progression/stall checks suppressed, this is expected, not a null result").
- **The single biggest risk: an automated reviewer asked to produce recommendations will
  produce recommendations, whether or not there's anything to say.** This is a known
  failure mode of any periodic-report system (it's why RP/Juggernaut-style apps sometimes
  get criticized for churning suggestions). The report format must make "nothing changed,
  keep going" a legitimate, first-class output — not a degenerate case the template makes
  awkward to write. Every check in §3 has an explicit "within range, no action" outcome;
  the report template should default to that language rather than requiring the loop to
  invent a reason to say something.
- **Public-profile route is undocumented-as-an-API.** If Liftosaur changes the markup,
  the parser breaks. It should error loudly into the report ("pull failed, no data this
  week") rather than silently reusing last week's cached pull and presenting stale numbers
  as current — a fail-fast requirement per `AGENTS.md`'s Code section.
- **Volume-adherence check (check 3) depends on Liftosaur's per-exercise data mapping to
  the right primary muscle correctly** — `liftosaur.md` already documents the app's own
  synergist-credit numbers disagree with `program.md`'s primary-target counting. The
  checker must implement `program.md`'s counting convention itself from the raw per-exercise
  set log, not read any pre-aggregated "volume per muscle" number the app might expose,
  or it will silently inherit the app's wrong (synergist-inclusive) convention.
