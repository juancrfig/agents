# Handoff — 17 Pending Memory Requests

**Date:** 2026-08-20 · **Author:** Hermes Agent (default profile)
**Status:** For discussion — nothing approved/rejected yet
**Why this exists:** `memory.write_approval: true` in config.yaml means every memory write is staged
under `~/.hermes/pending/memory/` instead of being applied. These 17 accumulated over **Aug 18–20**
from three sources: `assistant_tool` (agent-initiated during tasks), `background_review` (background
session reviews), and one session's own additions.

**How to act on them:** run `/memory pending` in the chat — it walks the queue and lets you approve
or discard each item. The IDs below match the queue entries.

---

## Summary

| Cluster | Items | Unique facts | Recommendation |
|---|---|---|---|
| 🏋️ Gym | 6 | ~3 | Approve 3, skip 3 (dupes) |
| 👨‍💻 Work profile | 4 | ~2 | Approve 2, skip 2 (dupes/conflict) |
| 💻 System | 3 | 3 | Approve 3 |
| 📁 Projects | 4 | 4 | Approve 4 |

**Net: approve ~12, skip ~5.** Heavy duplication — 5 of the 17 say roughly the same thing.

---

## 1 · 🏋️ Gym cluster (6 items)

### 4f6edd8c — baseline gym entry
- **origin:** assistant_tool · **created:** 2026-08-20 17:55 · **target:** user profile
- Logs workouts as compact blocks (zone / exercise / done-expected-sets / rest). Wants next-session
  targets (progressive overload). Handled by pinned skill `gym-progress-tracker`; data at
  `~/.hermes/gym/gym-log.json`.
- **Verdict: SKIP** — `7fd9b4d4` below is a strict superset that *replaces* this exact entry.

### 7fd9b4d4 — gym entry v2 (replace) + succinct/bilingual
- **origin:** background_review · **created:** 2026-08-20 18:50 · **target:** user profile
- **op 1 (replace):** Juanes (Juanes Figueroa) trains at the gym; logs in compact blocks **or loose
  prose**. Progressive overload: hit target reps → increase weight, reps reset to 8. Does dominadas +
  calves frequently regardless of muscle-day. Machine weights in "units" (bench press 10u) **or** kg
  (dominadas 18kg). Pinned skill, data path.
- **op 2 (add):** Ultra-succinct replies while at the gym (1–2 lines, target number front and center).
  Bilingual Spanish/English, code-switches freely — mirror his language.
- **Verdict: ✅ APPROVE** — canonical gym entry. Supersedes 4f6edd8c.

### 93e7e6db — succinct + loose logs
- **origin:** background_review · **created:** 2026-08-20 18:04 · **target:** user profile
- **op 1:** Ultra-succinct replies during workouts — no time to read long messages.
- **op 2:** Logs arrive loose: weight kg (own line or trailing), rest on the reps line ("12/12/4 1min
  descanso"), Spanish terms (descanso, series), zone often omitted, logs may be backdated or "tonight" —
  confirm date before storing.
- **Verdict: SKIP** — op 1 duplicates the succinct preference; op 2 is procedural detail already
  documented in the pinned skill (rest formats, backdating, Spanish parsing).

### 5a80af61 — succinct
- **origin:** background_review · **created:** 2026-08-20 19:46 · **target:** user profile
- Succinct replies during gym: logged numbers, next targets, short confirmation. No walls of text.
- **Verdict: SKIP** — third occurrence of the same preference.

### 027b65d4 — succinct + Spanglish energy + incremental sets
- **origin:** background_review · **created:** 2026-08-20 19:41 · **target:** user profile
- **op 1:** Extremely brief replies at the gym; reports sets **one at a time** and expects the tracker
  to update the session incrementally.
- **op 2:** Communicates in casual Spanglish with slang and emojis (e.g. "DONE MOTHERFUCKER"); match
  that informal energy; exercise names may be prose; weight in kg or machine "units".
- **Verdict: ✅ APPROVE (condensed)** — the Spanglish/energy style is a genuinely unique, high-value
  fact. The incremental-set reporting is already in the skill's per-set logic.

### 84c65b4a — long-run dataset integrity
- **origin:** assistant_tool · **created:** 2026-08-20 19:58 · **target:** user profile
- Building a long-run gym dataset for data analysis: strict per-session date accuracy, zero mixing of
  exercises across sessions. Never present reminders/targets from different dates as one list.
- **Verdict: ✅ APPROVE**

**Gym cluster net: approve 7fd9b4d4, 027b65d4 (condensed), 84c65b4a. Skip 4f6edd8c, 93e7e6db, 5a80af61.**

---

## 2 · 👨‍💻 Work profile cluster (4 items)

### d9165a27 — engineer + PR pain + book
- **origin:** background_review · **created:** 2026-08-20 13:26 · **target:** user profile
- Software engineer; primary interface to job codebase is AI agents (asks questions, reviews
  AI-generated PRs); architecture organizationally fixed (repository/service/provider), cannot change.
  Pain point: unexpected PR surprises. Was reading *A Philosophy of Software Design* but paused,
  fearing overstudying.
- **Verdict: SKIP** — covered by 6fda65d2 (superset, created 16 min later). The "paused the book"
  detail is contradicted by 6fda65d2's "currently studies" — see conflict note below.

### 6fda65d2 — engineer profile v2 (4 ops)
- **origin:** background_review · **created:** 2026-08-20 13:42 · **target:** user profile
- **op 1:** Software engineer; fixed Repository/Service/Provider architecture; no authority over
  system design at his job.
- **op 2:** AI agents have been his main interface to the codebase ~6 months; recurring "unexpected
  surprises" in AI-generated PRs is the pain point, driving study of deep code comprehension vs
  code-unread agentic workflows.
- **op 3:** Studies software design fundamentals (Ousterhout's *A Philosophy of Software Design*),
  follows Uncle Bob and Matt Pocock; keeps an Obsidian wiki at `/home/juancrfig/wiki` (llm-wiki) with
  `concepts/` and `raw/` for research syntheses.
- **op 4:** Prefers **adversarial multi-agent analysis**: dispatch opposing research to the Horus
  profile, then staged debates between multiple Hermes instances (asked for gpt-5.6-sol via
  openai-codex at low reasoning) with fixed reply counts and a joint recommendation document.
- **Verdict: ✅ APPROVE**
- ⚠ **Conflict to resolve:** op 3 says "currently studies Ousterhout"; d9165a27 (13 min earlier) says
  he *paused* it fearing overstudying. Treat op 3 as the current state.

### 238ca7a6 — deterministic verification
- **origin:** assistant_tool · **created:** 2026-08-18 21:08 · **target:** user profile
- Prefers deterministic verification over assumed completion. For multi-step/bootstrap work wants
  idempotent scripts + dry-runs + rollback-to-fresh + machine-checkable verification (CLI output,
  counts, hashes). "Done" must be evidenced, never assumed. Believes prompt engineering has limits;
  deterministic control wins on critical paths.
- **Verdict: ✅ APPROVE**

### 5db67e66 — decision records preserving WHY
- **origin:** background_review · **created:** 2026-08-20 06:06 · **target:** user profile
- Wants decision records preserving WHY: verbatim questions quoted, one Decision per topic with
  rationale grounded in research; unused options framed as "deferred, not rejected" with a concrete
  follow-up criterion (e.g. Grok Build vs Codex). Worker/agent observations are evidence, never proof.
- **Verdict: ✅ APPROVE**

**Work cluster net: approve 6fda65d2, 238ca7a6, 5db67e66. Skip d9165a27 (superseded).**

---

## 3 · 💻 System cluster (3 items)

### fe25e003 — desktop environment
- **origin:** background_review · **created:** 2026-08-19 20:19 · **target:** memory
- Omarchy (Arch) + Hyprland (Wayland, Lua config) + fcitx5 on ThinkPad E490 (hostname PadE490).
  Keyboard input flows through fcitx5; `hyprctl keyword` is a no-op on the Lua config (**use
  `hyprctl eval`**). `~/Projects/Omarchy` is a git repo; `overlay/` is source of truth for `~/.config`
  and `~/.local`; its AGENTS.md documents the keyboard-layout system.
- **Verdict: ✅ APPROVE**

### a5d2ccb8 — US keyboard layout
- **origin:** assistant_tool · **created:** 2026-08-19 21:21 · **target:** user profile
- Wants all keyboards fixed permanently to the US layout; no automatic LATAM/USB switching.
- **Verdict: ✅ APPROVE** — complements fe25e003.

### 0443baf5 — Telegram gateway runs manually
- **origin:** background_review · **created:** 2026-08-19 21:17 · **target:** memory
- Telegram is configured (TELEGRAM_BOT_TOKEN + TELEGRAM_ALLOWED_USERS in `~/.hermes/.env`) but run
  manually, **not** a systemd user service — after reboot/logout the bot is down until the gateway is
  restarted.
- **Verdict: ✅ APPROVE**
- **Open question:** do you want this fixed (install as a systemd service) or is manual fine?

---

## 4 · 📁 Projects cluster (4 items)

### 4e8d06d7 — vault location
- **origin:** background_review · **created:** 2026-08-20 06:06 · **target:** memory
- Vault is a git repo at `~/Projects/vault` (pushed to GitHub via SSH), NOT `~/Documents/Obsidian
  Vault`. Numbered top-level folders: `1 - Projects/<Domain>/<Project>/`, `5 - Journal/Days/`,
  `Media/`. AI-engineering projects live under `1 - Projects/AI Engineering/`. The repo has unrelated
  untracked journal/media files that must not be committed.
- **Verdict: ✅ APPROVE**

### dce87091 — Evidence Factory project
- **origin:** background_review · **created:** 2026-08-20 00:43 · **target:** memory
- Evidence-driven AI software-delivery system at `~/Projects/evidence-factory-worktrees/bootstrap`
  (per-ticket git worktrees, Codex workers, deterministic gates, SQLite audit + JSONL events,
  versioned Markdown evidence reports). Core stance: Hermes supervises only — factory never
  auto-merges; "merged" status is a recorded human outcome.
- **Verdict: ✅ APPROVE**

### de3e5de6 — "agentic system" = Evidence Factory
- **origin:** background_review · **created:** 2026-08-20 19:46 · **target:** memory
- "Agentic system" = Evidence Factory: live impl at `~/Projects/vault-evidence-factory` (branch
  `feat/evidence-factory`); bootstrap source at `~/Projects/evidence-factory-worktrees`; Codex CLI is
  the worker harness. **Distinguish from:** `~/Projects/the-agent` (stock Hermes profile repo) and
  `~/Projects/agents` (the agent roster — this repo).
- **Verdict: ✅ APPROVE**

### eb2a0e3d — recurring message annotations
- **origin:** assistant_tool · **created:** 2026-08-19 23:08 · **target:** memory
- Annotations on recurring messages (e.g. the 05:05 Telegram mobility routine to chat 6595639106):
  generate fresh each time by reading the latest journal entry in `~/Projects/vault/5 - Journal/Days/`,
  picking something interesting, in your own words and tone — never a transcript of the entry.
  Context matters (who reads it, when, on what occasion).
- **Verdict: ✅ APPROVE**

---

## Consolidated recommendation

| Action | IDs |
|---|---|
| ✅ Approve (12) | 7fd9b4d4 · 027b65d4 · 84c65b4a · 6fda65d2 · 238ca7a6 · 5db67e66 · fe25e003 · a5d2ccb8 · 0443baf5 · 4e8d06d7 · dce87091 · de3e5de6 · eb2a0e3d — *(13 with 027b65d4; see note)* |
| ⏭ Skip — duplicate/superseded (5) | 4f6edd8c (superseded by 7fd9b4d4) · 93e7e6db (dup) · 5a80af61 (dup) · d9165a27 (superseded by 6fda65d2) |

*Counts: 027b65d4 contributes 2 facts (succinct+Spanglish) but can be condensed into one entry.*

## Open questions for discussion

1. **Tone matching** — 027b65d4 wants informal Spanglish energy matched ("DONE MOTHERFUCKER"). To
   what extent in the desktop chat vs other surfaces (Telegram)? Always, or only when he's mid-set?
2. **Conflict** — Ousterhout book: actively studying (6fda65d2) or paused (d9165a27)? Resolve to
   "currently studying" unless you say otherwise.
3. **Telegram gateway** — leave manual, or install as a systemd user service so it survives reboot?
4. **Memory vs skill split** — gym parsing details (loose logs, rest formats, backdating) already
   live in the pinned skill. OK that memory only holds *preferences* (succinct, Spanglish, dataset
   integrity), not mechanics?
5. **Machine "units"** — bench press logged as 10u. Confirmed it should stay in units, not converted
   to kg?

## Appendix — raw queue (17 files)

```
027b65d4  batch  user  2026-08-20 19:41  background_review   succinct + Spanglish + incremental sets
0443baf5  add    mem   2026-08-19 21:17  background_review   Telegram gateway manual, not systemd
238ca7a6  add    user  2026-08-18 21:08  assistant_tool      deterministic verification preference
4e8d06d7  add    mem   2026-08-20 06:06  background_review   vault git repo at ~/Projects/vault
4f6edd8c  add    user  2026-08-20 17:55  assistant_tool      gym baseline (superseded)
5a80af61  batch  user  2026-08-20 19:46  background_review   succinct replies (dup)
5db67e66  add    user  2026-08-20 06:06  background_review   decision records preserving WHY
6fda65d2  batch  user  2026-08-20 13:42  background_review   engineer profile v2 (4 ops)
7fd9b4d4  batch  user  2026-08-20 18:50  background_review   gym entry v2 + succinct/bilingual
84c65b4a  add    user  2026-08-20 19:58  assistant_tool      gym dataset integrity
93e7e6db  batch  user  2026-08-20 18:04  background_review   succinct + loose logs (dup)
a5d2ccb8  add    user  2026-08-19 21:21  assistant_tool      US keyboard layout permanent
d9165a27  add    user  2026-08-20 13:26  background_review   engineer profile v1 (superseded)
dce87091  add    mem   2026-08-20 00:43  background_review   Evidence Factory project
de3e5de6  batch  mem   2026-08-20 19:46  background_review   agentic system = Evidence Factory
eb2a0e3d  batch  mem   2026-08-19 23:08  assistant_tool      recurring message annotations
fe25e003  add    mem   2026-08-19 20:19  background_review   desktop env (Omarchy/Hyprland/fcitx5)
```
