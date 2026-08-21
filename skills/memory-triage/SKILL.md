---
name: memory-triage
description: "Use when Hermes identifies a possible persistent memory."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [memory, pending, approval, triage, dedupe, handoff]
    related_skills: [session-librarian, hermes-agent]
---

# Memory Triage

When `memory.write_approval: true` is set in `~/.hermes/config.yaml`, every memory write stages to a
pending queue instead of applying. Queues accumulate fast — both `background_review` sessions and
`assistant_tool` writes stage there. This skill covers locating and reading the queue, deduping and
clustering it into verdicts, and producing a review handoff doc the user can act on. (Seen in the wild:
17 files staged over 3 days, of which only ~12 were unique facts.)

## When to use

- User mentions `/memory pending`, "memory requests", "staged memory", "approve memory", "pending writes".
- The memory tool returns `staged for approval` / `pending_id` instead of applying.
- A memory batch add is rejected for size and needs consolidation, or the user wants to prune what's being saved.

## Queue mechanics

- Location: `~/.hermes/pending/memory/*.json` — one file per staged write.
- File schema (v1): `id` (hex), `created_at` (epoch seconds), `origin` (`assistant_tool` | `background_review` | other), `target` (`user` profile vs `memory` store), `action` (`add` | `batch` | `replace` | `remove`), `summary` (one line, often truncated), `payload` holding the operations — for `batch`, `payload.operations[]`, each `{action, content|new_text, old_text?}`.
- The user acts on the queue with `/memory pending` in chat. The agent cannot approve on its own — never hand-delete pending files as a shortcut; the queue IS the user's review surface.
- **Count ops, not files**: one `batch` file can carry 2–4 distinct facts.

## Triage workflow

1. **Enumerate + hydrate.** Run `scripts/list_pending.py` (or an execute_code loop over the dir) for id / created_at / origin / action / target / summary. Then read each file's FULL payload — summaries are truncated and hide the real content, especially in batch ops.
2. **Cluster by domain.** Group items by topic (e.g. gym, work profile, system env, projects). Background reviews often emit several related items in a burst — cluster by origin + timestamps too.
3. **Recency and supersession.** A newer request that updates, replaces, or contains an older request automatically supersedes the older one. Reject the older request; do not preserve both.
4. **Dedupe via superset analysis.**
   - A `replace` op whose `old_text` matches an earlier `add` supersedes it → skip the older add.
   - The same preference stated 2–3× (e.g. "succinct replies") → keep the richest entry, skip the rest.
   - A `batch` item that bundles a duplicate and a unique fact → evaluate the operations separately when possible.
5. **Correct routing.** Distinguish facts about the user from instructions about Hermes behavior. A desired agent behavior, tracker outcome, parsing rule, or task constraint is not a `USER.md` fact merely because it arose from a user request. Route reusable procedures to skills, project facts to project context, and job-specific instructions to the relevant cron prompt.
6. **Operational specificity.** Reject vague personality or style labels such as “uses slang,” “uses emojis,” or “speaks Spanglish” when they leave context, intent, or usage conditions unspecified. A general user fact must still be concrete enough to avoid inventing details about the user.
7. **Flag genuine conflicts, don't silently resolve.** Same fact stated two ways across origins (e.g. “currently studying book X” vs “paused book X”) → report “cannot decide” and let the user choose.
8. **Verdict table.** Per item: ✅ approve / ✏️ modify / ⏭ skip-dupe / ⏭ skip-superseded / 🔀 reroute / ⚠ cannot decide. Give a per-cluster net count only after counting operations consistently.

## Handoff doc

When the user asks for a doc to discuss the queue (their preferred review format), use `templates/memory-handoff.md`. Structure:

- Header: date, author, why the queue exists, how to act (`/memory pending`).
- Summary table: clusters × item counts × unique-fact counts × net verdict.
- Per-cluster detail: each item with origin, created, full content, verdict + rationale.
- Consolidated recommendation table.
- **Open questions** — always include: tone/style limits, conflicts, config decisions only the user can make (e.g. “should X be a service?”).
- Appendix: raw one-line-per-file queue listing.

## Pitfalls

- `created_at` is epoch seconds — convert with datetime. Ordering matters for superset detection (a `replace` usually lands minutes after the `add` it supersedes).
- Don't judge from `summary` alone — it is truncated mid-sentence.
- The queue keeps growing while write-approval stays on — triage is recurring, not one-shot. If a user dislikes the noise, suggest raising approval to only external-side-effect writes.
- Don't confuse with `session-librarian` (session history store) — pending memory is a different store with a different review surface.
- There is no bulk-approve CLI; `/memory pending` walks every file. The verdict table is what makes the walk fast.

## Support files

- `scripts/list_pending.py` — enumerate the queue (id, time, origin, action, op count, summary). Run this first, then read full payloads of the interesting ids.
- `templates/memory-handoff.md` — handoff doc skeleton (clusters, verdicts, open questions, appendix).
