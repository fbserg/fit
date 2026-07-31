# Publishing decision record

## EXECUTED 2026-07-31 — what actually happened

This document was written as a plan. It has now been run, and reality differed from it in four
ways worth recording rather than quietly patching.

**1. The scale was underestimated.** The plan says 11 commits, 9 carrying session links. By
execution time it was **24 commits, all 24 carrying them** — the repo kept being worked on after
the audit. Any count in a document like this is a snapshot, not a fact; re-derive it at execution
time. This is the same failure mode as trusting a stale scan.

**2. This file was itself the largest remaining PII leak.** It quoted both the personal gmail and
the employer address verbatim, in full, several times — while instructing the reader to never let
those addresses touch the repo. An audit document that names what it is protecting becomes the
thing that needs protecting. All addresses and session IDs here are now redacted placeholders.

**3. The scan image carries a device serial the audit missed.** Human inspection (checklist step 6)
confirmed **no name field** — the plan's main worry was unfounded. But the footer carries
`270-2DM-<serial>`, a device serial that plausibly ties to one specific facility, which no item in
the table below mentions. Doesn't change the action (drop the image), does mean the table was not
exhaustive.

**4. The identity question was never asked, and it dominates everything else.** This entire
document reasons about which numbers to redact, and never asks *which GitHub account publishes the
repo*. That single choice dominates every redaction decision in the table: under a pseudonymous
account the body-composition numbers are anonymous and can all stay; under a named account they are
attributable no matter how the files are written, and no amount of in-file redaction changes it.

**Decision taken: named account, identity bundle only.** The body-composition numbers, program and
training analysis stay public and are knowingly attributable to a named person. Removed: the scan
image, `profile.md`, exact age, all email addresses, all session URLs, and the entire git history
that carried them. The residual-risk section below still applies and is now a *chosen* risk rather
than an unexamined one.

**Actions completed:**

| Step | Result |
|---|---|
| Backup before rewrite | `git bundle --all` written outside the repo |
| `private/` created, gitignored | Scan image + real `profile.md` moved there, still on disk locally |
| `profile.example.md` added | Public template; `profile.md` path now gitignored |
| Emails + session IDs redacted | Whole working tree greps clean |
| Exact age generalized | `README`, `CLAUDE.md`, `swimming.md` |
| History rewritten | Squashed to a single commit, no session links, non-personal author address |

## Recommended posture

1. **Do not push the current `.git` history as-is.** Every one of its 11 commits carries a
   real email address, and 9 of them carry links to the live chat transcripts that produced
   the repo — neither is removable by editing files in a new commit; both live in the commit
   objects themselves.
2. **Before the first push:** squash to a fresh single commit (or start a new orphan
   history) authored under a pseudonymous git identity, with commit-message bodies that
   contain no session links. No remote is configured yet (`git remote -v` returns nothing)
   and there are zero collaborators or forks — this is the cheapest possible moment to do
   this; it gets much harder the instant it's pushed.
3. **Drop the scan image** (`scans/2026-07-27-inbody270.png`) from what gets published, or
   publish a redacted crop. `scans/scans.md` already carries every number from it as text,
   with none of the image's printed-ID / handwriting / exact-age-height-timestamp exposure.

Everything else in the repo — detailed body-composition numbers, protein/calorie targets,
the training schedule's *structure*, injury canaries, quoted personal preferences — stays.
It's the worked-example content that makes the playbook credible, and none of it
individually re-identifies a stranger.

## PII item table

Merges the original audit and the adversarial critique. Where they disagreed, the
**Ruling** column states which one wins and why — no averaging.

| File | What | Risk | Decision | Reasoning / ruling |
|---|---|---|---|---|
| git history — commit author/committer lines, all 11 commits, both branches | `<redacted personal gmail>`, timezone `-0400` on every commit | **High** | **Rewrite/remove before any push** | Real email baked into every commit object. Deleting content in a future commit does not remove it from prior commits — only history rewrite (squash to one commit, orphan branch, or `git filter-repo`) does. No remote exists yet, so this is free today. |
| git history — commit message bodies, 9 of 11 commits | Two distinct `Claude-Session: https://claude.ai/code/session_...` URLs (`<session-id-A>` x4, `<session-id-B>` x5), plus full prose descriptions of the work | **High** | **Remove — strip from history rewrite, don't just avoid in new commits** | **Critique caught something the original audit missed entirely**: the audit inspected only author/committer lines, never message bodies. Verified directly in this session (`git log --all --format='%H%n%B'`): confirmed present in 9 of 11 commits. Whether these URLs are dereferenceable by a stranger (vs. requiring the account owner's own auth) is unverified — treat as high risk by default since removal is free and the downside of guessing wrong is a leaked full chat transcript, which could contain far more than what got distilled into the polished docs. Any history rewrite must clear message bodies too, or it only half-solves the problem it set out to solve. |
| `scans/2026-07-27-inbody270.png` | Printed InBody report: 10-digit ID field, height, age 33, sex, exact test timestamp (07.27.2026 18:16) | **High** | **Remove or heavily crop before publishing** | **Ruling on a real disagreement**: the audit characterized the ID field as "likely a gym/clinic member ID... tied to a specific facility's records system." The critique correctly calls this oversold — direct inspection shows a bare 10-digit number with no visible facility link; on many InBody kiosks this is a per-session test number, not a persistent account ID. **Ruling: critique wins on the characterization** (describe it as "a unique printed identifier of unknown scope," not a confirmed facility account ID) but **the audit wins on the action** — redact/crop regardless, since the combination of exact age + height + timestamp + a handwriting sample is independently sufficient justification, and the fix costs nothing (every number is already in `scans.md` as text). |
| `scans/2026-07-27-inbody270.png` | Handwritten pen annotations: "170g pro/day, 70g fats", "1700+400+300=2400 cal/day" | Medium | Remove (covered by not publishing the raw image) | Handwriting is a weak biometric (forensic comparison), and the numeric content is fully captured in `CLAUDE.md`'s nutrition rulings prose already. Nothing lost by dropping the image. Confirmed via `exiftool`: no embedded EXIF/GPS/camera metadata in the PNG — the only exposure is the visible printed/handwritten content, not hidden metadata. |
| `CLAUDE.md` Profile line: "Male, 34..., 5'10\" (178 cm), 154 lb, relatively fit, returning to consistent training after a gap." | Age/height/weight/sex bundled with training-return status | Medium | **Keep as-is — reject the audit's "generalize" recommendation** | **Ruling on a real disagreement**: the audit recommended rounding to "mid-30s, ~5'10\", ~155 lb." The critique is right that this is close to security theater — `scans.md` is being kept with the *identical* weight and body-fat % at full precision two sections later (it has to be, or the BMR/TDEE worked example breaks), so rounding the one-line summary removes essentially no re-identification risk while degrading the paragraph that sets up the derivation. **Ruling: critique wins — keep exact numbers everywhere or nowhere; picking one line to round is inconsistent and pointless.** |
| `CLAUDE.md` "No known kidney/metabolic issues" | Absence-of-condition statement | Low | Keep | States absence, not a diagnosis. Relevant to the high-protein-safety reasoning; both audit and critique agree, no dispute. |
| `scans/scans.md` (full file) | Full InBody readings: weight, TBW, LBM, fat mass, PBF, SMM, LBM, BMI, BMR, SMI, segmental lean per limb, raw bioimpedance values, two dated scans | Medium | Keep | This is the entire evidentiary basis for the derivation-chain teaching point (`PLAYBOOK.md` step 1) — removing it guts the worked example. Not independently identifying; becomes a risk only combined with the scan image or an external identity link. Audit and critique agree. |
| `program.md`, `exercises.md`, `swimming.md`, `abs.md` — third-person "he/his," age callout ("A 34-year-old can plausibly still swim at 74"), quoted first-person preferences | Sex, reiterated age, distinctive quoted phrasing | Low | Keep | Adds no new precision beyond the Profile line already covered above. Distinctive phrasing only helps an attacker who already suspects the author and has other writing samples to match against — a stretch attack, not a primary vector. The quotes are also exactly what makes the playbook's "here's how a real constraint shaped a real decision" content credible. Audit and critique agree. |
| Fixed weekly training/testing cadence (`CLAUDE.md` Measurement protocol, `program.md` "same four days/times each week," `swimming.md` prescription) | Cadence pattern, no concrete days/times/location anywhere in the text | **None — no action** | **Keep, reject the audit's "generalize" recommendation** | **Ruling on a real disagreement**: the audit rated this medium/generalize. Direct grep for day names, clock times, or a location in `program.md` found zero — the text only ever says "same four days/times each week" as an abstract adherence principle, and the audit's own reasoning admits this ("the doc correctly stays abstract... this is good"). **Ruling: critique wins — there is nothing concrete left to generalize.** Reframed as a guardrail below, not an open item. |
| `liftosaur.md` share link `liftosaur.com/p/14002621` | Public program link, no account required per the doc | Low | Keep, with a caution note | Not currently account-bound per the doc's own statement. Central to the playbook's "program as executable code" pitch. One-line caution: use a fresh/logged-out session if the link is ever re-edited before or after publishing, so it doesn't retroactively bind to a personal account. |
| Injury canaries ("anterior shoulder pain / lost internal rotation, or stalling reps") | Prospective monitoring guidance | Low | Keep | Precautionary, not a disclosed diagnosis or current condition. Central to the risk-management method. Audit and critique agree. |
| `userEmail: <redacted employer address>` (session context only — confirmed absent from every repo file and from `git log --all` via grep) | Business email tied to a named employer, not present in the repo | Low, not a repo item | No repo action; guardrail only | Not in any tracked file or commit. Flagged only so the human is aware: if this address or its domain is ever pasted into a repo file, commit, or used as the git commit identity during the history rewrite below, it becomes a far stronger identity link than the existing `<redacted personal gmail>` — it points at a named organization. **Do not use it as the git identity when rewriting history.** |
| Device model, `InBody 270 (2-frequency BIA, 20/100 kHz, 8-point electrodes)` | Equipment make/model | None | Keep | Not personal data. Load-bearing for the BIA-derivation methodology point. |

## The git history problem, stated plainly

**What survives a file deletion:** everything. Deleting or redacting a file in a new commit
does not remove it from the objects of any prior commit. The email address and session
links are in commit metadata and commit messages from `c18ff1a` (2026-07-27) through
`39e9490` (2026-07-31) — all 11 of them, on the only branch that exists (`main`). Verified
directly: `git log --all --format='%H%n%B'` shows the `Claude-Session:` line in 9 of the 11
commit bodies, and every commit's author line reads `<redacted personal gmail>`.

**What GitHub caches even after a history rewrite (per GitHub's own docs):**
- Pull-request diff views reference the *original* commit SHAs internally. Rewriting
  history does not clear these — GitHub explicitly states this requires a **support
  ticket** (repo name, affected PR count, "First Changed Commit(s)" list from
  `git filter-repo`'s output) before they'll dereference/delete the cached views. Not
  applicable here yet, since nothing is public — but it means "rewrite after pushing" is a
  break-glass remedial action with real coordination cost, not something to lean on.
- **Forks are permanently uncontrollable by the origin owner.** If a commit exists in
  anyone's fork, GitHub cannot remove it from that fork; only the fork owner can. This is
  the strongest argument for getting history right *before* the first push rather than
  treating it as fixable later.
- Any collaborator with an old clone who does a plain pull-then-push after a rewrite
  silently reintroduces the purged commits.

**Concrete options, with real costs, given the current state (no remote, no forks, no
collaborators — confirmed via `git remote -v`):**

| Option | Cost | When it's right |
|---|---|---|
| Squash all 11 commits into one fresh initial commit, authored under a pseudonymous identity, message body scrubbed of session links | Trivial — no coordination needed, nothing to leave stale, since nothing has ever been pushed | **Default choice here.** Zero collaborators/forks means there is no rewrite-after-push penalty to avoid; do the cheap version now. |
| `git filter-repo` to rewrite author identity across all 11 commits in place, keeping individual commit boundaries | Moderate — need to also separately edit each message body (filter-repo's default mode doesn't touch bodies) | Only worth it if the individual commit-by-commit history (not just the final state) has standalone value to a reader; it doesn't obviously here. |
| Push as-is, rewrite later if it becomes a problem | High, and rising — once public, "never rewrite public history" is the standing practitioner consensus; a later rewrite needs the GitHub support ticket path above, and can't touch forks at all | **Reject.** No reason to accept a cost that's avoidable for free right now. |

## Pre-publication checklist

Run in order. Each step blocks the next.

1. `git remote -v` — confirm still empty before doing anything destructive to history; if a
   remote has been added since this record was written, stop and re-plan (the calculus
   above assumes nothing has been pushed).
2. `git log --all --format='%h %ad %an <%ae>' --date=iso` — reconfirm current commit count
   and identity on every commit (was 11 at the time of this writing; re-run since this repo
   is actively being edited by another agent).
3. `git log --all --format='%H%n%B'` — reconfirm which commits carry `Claude-Session:` links
   or other prose that might mention anything not in the polished docs (informal asides,
   other projects, names). Read the full output, not just grep for the known pattern.
4. Squash/rewrite history per the ruling above, using a placeholder identity
   (e.g. `anon <anon@users.noreply.github.com>` or a GitHub-provided noreply address) —
   never `<redacted employer address>` or any other real address.
5. `grep -riE '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}' .` across the working tree (excluding
   `.git`) — catch any email address left in file content, not just git metadata.
6. **Open `scans/2026-07-27-inbody270.png` and look at it with human eyes** — do not trust
   an automated pass for this. Confirm: is there a name field anywhere on the printout (not
   just the ID number already flagged)? Is there a photo embedded in the report itself?
   Automated tools (exiftool, grep) cannot read printed text in an image; only a human
   glance catches a name field.
7. Decide, based on step 6: drop the image entirely, or crop out every field except the
   composition-analysis panels needed for the derivation-chain teaching point. If cropping,
   re-run `exiftool` on the cropped output to confirm no metadata was reintroduced by
   whatever tool did the crop.
8. Re-read `CLAUDE.md`, `program.md`, `exercises.md`, `abs.md`, `swimming.md`, `liftosaur.md`
   end to end for anything not caught by the table above — a gym name, a city, a specific
   clock time, a coworker's name — none were found as of this writing, but the repo is being
   actively edited concurrently, so this must be re-checked against the final content, not
   this record.
9. Confirm `scans/2026-07-27-inbody270.png` file permissions (`ls -la scans/`) — currently
   `600` (owner-only), unlike every other file in the repo (`644`). That's a signal the file
   was already implicitly treated as more sensitive; if it ends up published at all, that
   instinct was correct and argues for the crop-not-drop approach, not the reverse.
10. Push, only after steps 1-9 are clean.

## What not to bother with

Rejected explicitly, with reasons — a checklist nobody follows because it is absurd is
worse than a short one that gets done.

- **Rounding the Profile line's age/height/weight to vague ranges.** Rejected above:
  `scans.md` keeps the exact same numbers at full precision a few lines later, so rounding
  one summary line is theater, not risk reduction. Keep exact numbers everywhere or accept
  they're everywhere — don't hedge on one line.
- **Redacting/generalizing the "fixed weekly schedule" language.** There is nothing
  concrete in it (no days, times, or location anywhere in `program.md` or `CLAUDE.md`) —
  confirmed by direct grep. Redacting an abstraction produces no security benefit, only a
  worse sentence.
- **Removing the third-person "he/his" pronouns or the quoted personal preferences from
  `program.md`/`exercises.md`.** These only assist an attacker who already suspects the
  author's identity and has independent writing samples to match against — a stretch
  attack far downstream of the git-history and scan-image fixes. Stripping them would also
  strip the quoted-constraint content that makes the playbook's worked examples credible.
- **Treating the InBody printout's ID number as a confirmed facility account identifier**
  and building special handling around that assumption (e.g. contacting the clinic to ask
  about their ID scheme). No visible evidence on the printout supports that specificity —
  it's a bare 10-digit number. Crop it because unique printed numbers on a public image are
  bad practice as a category, not because of a confirmed identity-database link that hasn't
  been established.
- **Filing a GitHub support ticket for cached PR-diff views before ever pushing.** That
  process exists for post-push remediation. Nothing has been pushed; there is nothing for
  GitHub to have cached yet. Doing history hygiene correctly *before* the first push makes
  this entire category of concern inapplicable, which is the point of doing it now.
- **Encrypting or gitignoring the numeric body-composition data (`scans.md`, the
  CLAUDE.md rulings) the way a dotfiles/secrets manager would.** The precedent research's
  chezmoi/plaintext-accounting comparison is a genuine structural analogy for the general
  *pattern* (public method, private instance data) but this repo's stated goal is publishing
  the instance data as a worked example, not hiding it — encrypting the very numbers the
  playbook exists to demonstrate defeats the purpose of publishing at all.

## Residual risk after the checklist

Not zero. Explicitly:

- **The combination of exact age/height/weight/sex, US-Eastern timezone (visible in any
  rewritten commit unless the rewrite also flattens the timestamp offset — flag this for
  the rewrite step), a fixed weekly training cadence, and precise body-composition data**
  is still a real quasi-identifier bundle for anyone who already suspects who this is and
  wants to confirm it. No amount of redaction removes this without also removing the
  worked-example numbers that are the entire point of publishing. This repo's honest
  position is: safe against a cold stranger browsing GitHub, not safe against a
  motivated acquaintance running a confirmation check.
- **Progress photos, if ever added per `abs.md`'s own prescribed measurement protocol
  (fixed-condition monthly photos), are a materially different risk category** from
  everything currently in the repo — a face-visible or backgrounded photo is queryable by
  reverse-image and facial-recognition tools in a way no number in this repo is. This
  checklist does not cover that case because no such photo exists in the repo yet; if one is
  added later, treat it under the same scrutiny as the scan image (step 6), not as routine
  data.
- **No documented case of concrete harm from voluntarily publishing personal
  body-composition data on GitHub was found during research**, which could mean the risk is
  genuinely low, or could mean the practice is obscure enough that no case has surfaced —
  the research could not distinguish these, and neither can this document.
- **Whether the Claude-Session URLs are dereferenceable by a stranger with the link is
  unverified.** Removing them from history (per the checklist) makes this moot for this
  repo, but if a similar link is ever pasted into a future public commit, verify
  dereferenceability first rather than assuming either direction.
