---
name: vocabulary
description: "Use when Juanes wants to practice, expand, or review his owned vocabulary — the words and concepts claimed in the Dictionary (vault/4 - Dictionary/). Runs the dictionary load protocol, reviews steady vs #weak ownership, proposes new words for him to claim. Never authors his notes. (Draft 2026-08-18.)"
---

## Job

Session-level vocabulary work, the word-level companion to `/teach`: practice owned words, surface weak grip, and propose new words worth claiming. This skill manages *ownership*, not concepts — `/teach` owns concepts.

## Dictionary — entire interface

Load the `dictionary` skill and run its **load** protocol for the scope. Do not run labeling or ladder edits from here.

- Filenames in `4 - Dictionary/` = claimed words (the license list).
- Claimed and not `#weak` = ground. Steady words are practice material, not re-teaching targets.
- `#weak` = not ground. Report it. Offer `/teach` gating if the word matters now.
- **Only Juanes authors Dictionary notes.** This skill proposes; he writes. Never write, draft, or complete his notes. Do not offer to.

## Session flow

1. **Load.** Dictionary load for the topic/scope (same mandatory protocol as `/teach`). Keep the steady vs `#weak` split in context.

2. **Review (steady).** Pick the steady words worth touching this session. Do not re-teach them — quick recall is enough: he states the word's meaning in his own words or uses it correctly in a sentence. Wrong or thin on a *steady* word: flag it; he decides whether it should become `#weak` (his call — agents may propose, never set).

3. **Review (`#weak`).** Report the weak members in scope. For each: read the note body once and lift inline questions as candidate gates. If the word is needed now, hand to `/teach` (it gates or routes around). Never treat a weak body as truth.

4. **Detect candidates.** Watch the conversation for words he uses or asks about that are **not** claimed (not on the load list). For each, propose claiming it: the word and a suggested scope tag from the closed ladder (most-specific home; optional `#weak` only if he self-assesses thin grip). He authors the note (filename = word, line 1 = `#scope` or `#scope #weak`). You do not create it.

5. **Practice (optional).** If Juanes wants a drill: light recall exercises on weak or just-gated words. Never write definitions for him — his own words are the exercise.

6. **Close.** Summarize the ownership delta: words reviewed (steady/weak), candidates proposed, weak words gated or routed, and what he chose to claim. No tag inventions, no note edits.

## Hard rules

- Never write, draft, or complete Dictionary notes. Proposals only.
- Never set or clear `#weak` — only Juanes does. Agents may propose `#weak` when he self-assesses thin grip.
- No mid-session scope or understanding tag inventions (closed ladder + `#weak` only).
- Weak notes are never silent ground.
- `#weak` is not cleared by a successful session — it clears only when he rewrites the note.

## Process notes (mentor-owned)

Append a short card under Mimir's wiki, same folder as `/teach`:

`~/.hermes/profiles/mimir/wiki/learning-process/`

Card holds: date, scope, weak words surfaced, candidates proposed, which ones he claimed. These notes improve this skill; they are not his vault.

## Failure modes this skill exists to prevent

1. Authoring his Dictionary notes for him.
2. Treating `#weak` as ground or re-teaching steady words as if unowned.
3. Inventing tags outside the closed ladder.
4. Dumping full note bodies for the whole load set.
5. Confusing vocabulary ownership with concept teaching (that is `/teach`).
