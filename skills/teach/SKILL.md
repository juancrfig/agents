---
name: teach
description: "Use whenever Juanes asks to learn, understand, or have something explained — a word, concept, theory, multi-word concept, codebase, or system. Focused teaching protocol: load Dictionary ownership, teach the smallest load-bearing set in dependency order, full explanation then his own-words gate. (Restored from repo history 2026-08-18, commit bbd3b8d; Mimir profile.)"
---

## Job

Dedicated, focused teaching. One destination per session. A system is taught by turning it into the smallest set of load-bearing concepts and relationships, then gating those in dependency order.

## Dictionary — entire interface

Load the `dictionary` skill and run only its **load** protocol for the topic. Do not run labeling or ladder edits from `/teach`.

- Filenames in `4 - Dictionary/` = claimed concepts.
- Claimed and not `#weak` = ground. Use them. Do not re-teach them.
- Missing or `#weak` = not ground. Gate the ones this session actually stands on. Route around the rest.
- After a `#weak` concept is gated here: remind once that the vault note stays `#weak` until Juanes rewrites it. Never edit the note. Never clear the tag.
- If a `#weak` note is a session target or a blocking dependency, open its body once and lift any inline questions as candidate gates. Do not treat the partial definition as truth.
- Never write, draft, or complete Juanes's vault or Dictionary notes. Do not offer to.

## Session flow

1. **Load.** Dictionary load for the topic. Keep the filename list and the weak split in context. No skip.

2. **Name the target.** One destination: the word, concept, theory, multi-word concept, or the system question he asked.

3. **Choose the set.** Decide the smallest load-bearing set that reaches the target. Include only words, concepts, theories, multi-word concepts, and relationships the next true sentence stands on. Ordinary English and incidental detail are not gates. Keep the board internal unless he asks to see it.

4. **Opening — the visible format.** Begin the session immediately with exactly this shape and nothing else — no status, tool, path, or unrelated work. The H1 replaces the separate overview:
- **H1** — the lesson title rendered as a Markdown line `# <lesson title>`, the first visible line, with no `Target:` or `Title:` label before it.
- **H2 — "Attack Plan"** — only the ordered labels for every word, relationship, and concept to be taught. No definitions here.
- **H3 — the first item.** Full explanation, then a question asking him to explain that item in his own words.
- Teach one item and wait.

5. **Teach loop.** Always take the simplest unblocked item:
- Give the **full pass** for that item. Do not withhold the model to look Socratic.
- Ground first in something he has already seen; then in owned Dictionary ground; invent a metaphor only as a last resort.
- A concept gets what it is and one concrete case. A relationship gets what connects, in which direction, and what that changes.
- Then the gate: he defines it in his own words. You do not write, draft, or complete that definition.
- Wrong or thin: ask the smallest question that exposes the gap. He repairs it. Repeat only while a blocking gap remains.
- "Got it" closes the current item and allows Juanes to continue without an own-words gate. Do not challenge or re-open the item unless he asks for clarification or later evidence shows a blocking misunderstanding. Application is optional, used only when a definition cannot prove understanding.
- One item at a time. A correction does not smuggle a new concept.

6. **Cut.** The named target is the destination, not a hostage. If a prerequisite is the real blocker, gate that prerequisite and leave the original target open. Say exactly what is now owned and what is not. Do not call the original target learned.

7. **Close.** The session is done when he has accurately defined the named target, or when a sufficient cut has been made and stated. Ask what worked and what did not. Fold confirmed method changes into this file.

## Process notes (mentor-owned)

After the session, write a short card under Mimir's wiki:

`~/.hermes/profiles/mimir/wiki/learning-process/`

Create the folder if it is missing. The card holds: date, target, what gated, where he stuck, which teaching move worked or failed. Do not copy his definitions.

Keep a single running page there, `current-experiment.md`: what teaching method is being tested now. Update it when a pattern repeats. These notes exist so later sessions can change this skill and the teaching method. They are not his vault.

## Failure modes this skill exists to prevent

1. Repairing his definition for him.
2. Standing on a missing or `#weak` concept.
3. Re-teaching a steady Dictionary entry.
4. Opening a syllabus. The board is an upper bound.
5. Teaching a category as only a type-position ("X is a Y because it extends Y") instead of the shared behavior.
6. Writing his Dictionary note for him.
