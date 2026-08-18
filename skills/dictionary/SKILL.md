---
name: dictionary
description: Useful to give a look at Juanes' vocabulary and his understanding of the universe.
---

# /dictionary — labeled vocabulary membership + load protocol

The words live in `vault/4 - Dictionary/`. This skill is the protocol for that folder, not a second word list.

Two jobs, in this order:

1. **Load (primary).** How those notes become a per-question license list: owned filenames, split into steady vs `#weak`. `/teach` runs only this job.
2. **Label (secondary).** How a note gets its one scope tag, optional `#weak`, and how the closed scope ladder may change. Used when Juanes authors or retags a note. `/teach` never runs this job.

This skill does not teach. It reports ownership. Teaching is `/teach`.


**Dictionary note**: vault file in `4 - Dictionary/`; filename = owned word (the license list). Line 1 holds tags only.

**Scope tag**: single most-specific short slug from the closed ladder (e.g. `#swe`, `#react`, `#linux`). Never long forms, never two scope tags on a note, never parents on the note.

**Understanding tag** (optional second tag on line 1): Juanes' self-assessed grip on that word. Closed set today: `#weak` only. Line shape: `#scope` or `#scope #weak`.

## Scope ladder (closed set — single source of truth)

Evolves only from real friction (new note that doesn't fit cleanly, repeated detection failures). Update skill + relabel notes atomically. Personal mental model first.

```
#fundamentals
  #engineering
    #swe
      #ai
      #devops
        #linux   (provisional)
      #web_dev
        #react
        #javascript  (when needed)
      #flutter   (under #swe directly, NOT under #web_dev)
      #db
  #math
    #stats
```

False homes rejected: `#flutter` under `#web_dev`; `#timezones` as root (use `#swe`); stacking `#fundamentals` on domain notes.

## Parent-walk table (compute load tag set)

Detected narrowest + every ancestor (incl. root). Extras are exact-tag only.

| Narrowest detected | Full load tag set (for default) |
|--------------------|---------------------------------|
| `#fundamentals`    | `#fundamentals` |
| `#engineering`     | `#engineering`, `#fundamentals` |
| `#swe`             | `#swe`, `#engineering`, `#fundamentals` |
| `#ai`              | `#ai`, `#swe`, `#engineering`, `#fundamentals` |
| `#devops`          | `#devops`, `#swe`, `#engineering`, `#fundamentals` |
| `#linux`           | `#linux`, `#devops`, `#swe`, `#engineering`, `#fundamentals` |
| `#web_dev`         | `#web_dev`, `#swe`, `#engineering`, `#fundamentals` |
| `#react`           | `#react`, `#web_dev`, `#swe`, `#engineering`, `#fundamentals` |
| `#javascript`      | `#javascript`, `#web_dev`, `#swe`, `#engineering`, `#fundamentals` |
| `#flutter`         | `#flutter`, `#swe`, `#engineering`, `#fundamentals` |
| `#db`              | `#db`, `#swe`, `#engineering`, `#fundamentals` |
| `#math`            | `#math`, `#fundamentals` |
| `#stats`           | `#stats`, `#math`, `#fundamentals` |

## Load protocol (A — primary; `/teach` always runs this)

1. **Detect narrowest scope**: Read the question/topic language against the closed ladder. Pick the most specific that honestly fits. If user explicitly supplies a tag (e.g. "dictionary load #react for ..."), use it. Refine if needed.

2. **Build load tag set**:
   - Default: the detected tag + all ancestors up the ladder to `#fundamentals`.
   - Optional extra scopes (e.g. `dictionary ... extra #economy`): for each extra use **exact match only** on the **first** (scope) tag. No ancestor expansion, no children. If an extra is unknown to ladder AND matches zero notes, report it ("no notes for unknown extra scope #X") — do not silently ignore or expand.

3. **Membership list (default payload)**: Filenames only (basename without .md) of every note in `4 - Dictionary/` whose **first line** starts with one of the load scope tags (optional understanding tag may follow on the same line).

   - **Never** dump full note bodies into context for the whole set. Open bodies only for specific words that are about to become anchors in an explanation, or that Juanes explicitly names.
   - Answer format: "Owned in scope (#detected + ancestors): list of filenames. (N total). Weak in set: … (or none)."
   - Always split the membership list into **steady** (no second tag) vs **weak** (`#weak` on line 1). Weak notes stay on the membership list (filename is still claimed) but are not ground until gated in `/teach`.

4. **Concrete shell recipe** (run via terminal tool to compute accurately; prefer this over mental list):

```bash
# Resolve the vault's 4 - Dictionary folder per-platform.
#   Linux:  ~/.vault/4 - Dictionary
#   Windows:  $HOME/Documents/GitHub/vault/4 - Dictionary
#             (the GitHub folder is assumed present under Documents)
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) DICT_DIR="$HOME/Documents/GitHub/vault/4 - Dictionary" ;;
  *)                    DICT_DIR="$HOME/.vault/4 - Dictionary" ;;
esac

# Build alternation for a load set, e.g. for #react branch
# Scope is always the FIRST tag; optional second tag is understanding only.
TAGS="react|web_dev|swe|engineering|fundamentals"
# First tag = scope (allows optional second understanding tag on same line)
rg --files-with-matches "^#(${TAGS})([[:space:]]|$)" "$DICT_DIR" \
  | xargs -I{} basename {} .md | sort

# Weak subset of that load set (line 1 is #scope #weak)
rg --files-with-matches "^#(${TAGS})[[:space:]]+#weak([[:space:]]|$)" "$DICT_DIR" \
  | xargs -I{} basename {} .md | sort
# Whole-Dictionary weak list:
rg --files-with-matches '^#[a-z_]+[[:space:]]+#weak([[:space:]]|$)' "$DICT_DIR" \
  | xargs -I{} basename {} .md | sort

# For exact extra only (no walk) — still first-tag match
rg --files-with-matches '^#economy([[:space:]]|$)' "$DICT_DIR" | xargs -I{} basename {} .md | sort

# Histogram of first (scope) tags
rg -N --no-filename -o '^#[a-z_]+' "$DICT_DIR" | sort | uniq -c | sort -nr
# Count understanding tags
rg -N --no-filename -o ' #weak' "$DICT_DIR" | wc -l
```

5. Unknown tags in extras: report, continue with what does match.

**Completion criterion**: The exact membership filename list for the computed load set has been produced (via recipe or equivalent), weak members are called out, and both are in context before any teaching starts. `/teach` has no "skip dictionary" path.

## Understanding tags (self-assessment)

Second tag on line 1 = Juanes' self-assessed understanding of that word. Orthogonal to scope. Not on the scope ladder. Never used for load membership or parent-walk.

| Line 1 shape | Meaning |
|---|---|
| `#scope` | Understanding good enough. Use as ground. |
| `#scope #weak` | Self-assessed weak. Filename still listed, but **not** ground. Body may still hold a thin definition **and open questions**. |

Rules:

1. **Absence = good enough.** No second tag means do not second-guess grip. Do not invent `#strong` / `#ok` marks.
2. **Only Juanes sets or clears understanding tags.** Agents may propose `#weak` when he says the grip is thin; never clear `#weak` after a session unless he says so. Clearing `#weak` is his call (usually after he rewrites the note). A successful `/teach` gate does **not** clear the tag.
3. **Closed understanding set (today):** `#weak` only. Do not invent new understanding slugs mid-session. Promote the set the same way as the ladder (skill edit + note pass) when real friction appears.
4. **Order on line 1:** scope first, understanding second. `#ai #weak` ✓. `#weak #ai` ✗. Two scope tags ✗. Understanding tag alone ✗.
5. **Not a dual scope tag.** `#fundamentals #swe` remains forbidden. `#swe #weak` is scope + understanding, not two homes.
6. **Weak bodies may contain questions.** A `#weak` note is allowed to mix a partial definition with open questions. That is expected, not dirty. When `/teach` opens on that word, **read the body and lift those questions as candidate gates**. Do not ignore them, and do not answer them outside `/teach` while treating the note as settled.

### Weak status — report, do not teach

When a note marked `#weak` is **about to be used**, do **not** treat it as ground.

**About to be used** means any of:

- About to open the note body as an explanation anchor
- About to treat the filename as owned/bare in a non-trivial way (building on it, teaching from it, or letting a design rest on it)
- Juanes names the weak word as the thing he wants to lean on right now

**Not "about to be used"** (report only):

- Mere membership listing during dictionary load ("Weak in set: Large Language Model")
- Passing mention while routing around it
- Flagging it as a Dictionary candidate without relying on its body

**What to do:**

1. Report which word is weak.
2. If this is already `/teach`, `/teach` decides whether to gate it or route around it.
3. If this is not a teaching session, do not teach it inline. Start `/teach` if the word must be owned for the work to continue; otherwise rephrase or pick a different owned word.
4. Never require the vault tag to be cleared before the session may use a just-gated concept as ground. Conversation gates the session; the note stays `#weak` until Juanes rewrites it.

When `/teach` opens a weak note, open its body once to lift inline questions as candidate gates. Still do not use the partial definition as gated truth.

## Labeling protocol (B)

When a new Dictionary note is authored (by Juanes), or when asked to propose/fix a tag for an existing one:

1. Identify the concept in the filename + (read only the tag area + first paragraph if needed; do not rewrite body).

2. Select **exactly one scope tag** from the closed ladder: the narrowest true home.
   - `#fundamentals` reserved for root-spine cross-domain notes that have no honest narrower home.
   - Most-specific wins (React hook → `#react`, not `#web_dev`).
   - If two homes tie equally: pick the one, or step up to shared parent, or split the note into two. Record the judgment call.
   - Never write parent scope tags on the note. Never two scope tags. Never long-form synonyms (`#software-engineering`, `#artificial_intelligence`, etc.).

3. Understanding tag (optional): keep existing `#weak` unless Juanes asks to change it; add `#weak` only if he self-assesses weak grip; omit second tag when good enough.

4. The tag line becomes (or is edited to) line 1: `#slug` or `#slug #weak`.

5. Heuristics (locked, apply judgment only if content clearly contradicts):
   - Root spine (System, cross-domain primitives with no narrower): `#fundamentals`
   - Engineering as craft/domain definition: `#engineering`
   - Complexity symptoms/causes, deep/shallow modules, interfaces, state, implementation, seams (design boundaries): `#engineering` (or `#swe` if purely software process)
   - SE-specific: modules, classes, functions, git, repos, interpreters, libs, encryption (general), waterfall/agile, headless, design patterns in code: `#swe`
   - DB/ORM/schema/migration/BLOB: `#db`
   - AI/LLM: `#ai`
   - Linux primitives (process, container, ssh, stdin, glob, daemon): `#linux`
   - Infra/scheduling (cron): `#devops`
   - Math/stats (stddev, asymmetric crypto math): `#math` or `#stats`
   - React specifics: `#react`
   - Flutter: `#flutter`
   - Time concepts used in SE (UTC, DST, local in code/config): `#swe`
   - EFIX/EXIF format note: `#swe`

6. Propose the change as a minimal tag-line-only edit. After Juanes approves, apply via targeted edit (only line 1 or the tag portion). Verify afterwards with rg that exactly one closed **scope** tag is first on line 1, optional `#weak` only as second tag, and no forbidden strings.

**Completion criterion**: Line 1 is `#scope` or `#scope #weak`; zero dual scope tags; zero long forms; body text is byte-identical except for the former tag line.

## Ladder edit protocol (C)

Ladder is living contract, not frozen and not invented on the fly.

1. Friction signal: a question whose best home isn't on ladder, or notes that keep getting dual-tagged in practice, or load returning surprising sets.

2. Propose the minimal ladder change (add leaf, promote, etc.). Update:
   - the diagram in this file
   - the parent-walk table
   - any examples/recipes here
   - the matching section in CONTEXT.md (keep in sync)

3. In the **same commit/change**: relabel every affected Dictionary note (tag lines only) to reflect new placement. Use the labeling protocol.

4. Never use a new tag in a running session before the SKILL.md edit + relabels are committed and bootstrapped.

5. Re-verify with the histogram recipe and load test for affected scopes.

6. Document the rationale briefly here or in an ADR under docs/adr/.

**Completion criterion**: SKILL.md + CONTEXT.md + all touched .md notes are updated consistently; `rg` on Dictionary shows only closed short tags; a test load for a previously-friction question now works cleanly.

## Integrations & hard rules

- `/teach` **always** (no optional) runs the LOAD protocol for the topic before any teaching. It references this skill by name and uses the returned filename list as the owned vocabulary baseline. Do not duplicate the ladder or load logic into teach/SKILL.md — pointer + mandatory call only.
- `#weak` is never silent ground. Dictionary reports it. `/teach` gates or routes around it. Other skills do not treat weak notes as steady anchors.
- software-architecture and other skills that need "what does he already own?" go through this. Weak members in the load set are reported and must not be used as silent foundations.
- Manual/widened: accept `/dictionary load "the question text" [extra #tag1 #tag2]`
- Shell recipes above are the ground truth for "what is tagged X" — use them; do not rely on stale mental model.
- Tag line is always line 1. First tag = scope (ladder). Optional second tag = understanding (`#weak` only today). Bodies use [[wikilinks]] for relationships.

## Verification checklist (run after any change)

- [ ] dictionary/SKILL.md frontmatter valid + description "Use when..."
- [ ] All 4 - Dictionary/*.md line 1 matches `^#[a-z_]+( #weak)?$` (exactly one closed-ladder scope tag; optional `#weak` only)
- [ ] `rg '#(software-engineering|software_engineering|web_development|artificial_intelligence|databases|mathematics|statistics|timezones)' "4 - Dictionary/"` returns nothing
- [ ] No note has two scope tags or `#weak` in first position
- [ ] Ladder in this file == ladder in CONTEXT.md
- [ ] Load recipe produces sensible filename lists for test cases (e.g. "react component", "linux process", "system") and surfaces weak members separately
- [ ] No mid-session tag inventions (scope or understanding)
