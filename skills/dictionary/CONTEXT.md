# Dictionary labeling and load

Shared language for tags on vault `4 - Dictionary/` notes, and for the skill that loads owned words by scope. Tags exist so an agent can answer "which words does Juanes already own for this question?" without re-teaching or skipping spine concepts. Connection-spotting can widen the load set on demand without hardcoding permanent cross-links.

## Language

**Dictionary note**:
A vault file in `4 - Dictionary/` whose filename is an owned word. Filenames are the license list; tags only place the word on the scope ladder.

**Scope tag**:
The single most-specific domain label on a note. Names where the word lives on the scope ladder. Canonical form is a short slug from the skill's closed list (examples: `#swe`, `#ai`, `#web_dev`, `#db`, `#math`, `#stats`). Always the **first** tag on line 1.
_Avoid_: topic tag (ambiguous), category (vague), full-path tagging, long synonyms (`#software_engineering`, `#software-engineering`, `#artificial_intelligence`, `#web_development`, `#databases`, `#mathematics`, `#statistics`)

**Understanding tag**:
Optional **second** tag on line 1. Juanes' self-assessed grip on that word. Closed set today: `#weak` only. Absence means good enough — do not invent `#strong` / `#ok`. Orthogonal to scope; never used for membership or parent-walk. Only Juanes sets or clears it. Weak note bodies may hold a partial definition **and open questions**; those questions feed `/teach` as candidate gates, not silent answers.
_Example_: `#ai #weak` on `Large Language Model.md`
_Avoid_: putting `#weak` first; two scope tags disguised as "understanding"; agent clearing `#weak` without his say; ignoring questions sitting in a weak body

**Scope ladder**:
A tree of scope tags owned by the skill. Root is `#fundamentals`. Multi-branch under the root. Notes store only the narrowest true home; the skill walks parents to the root at load time. The ladder is a living contract: it evolves from real use (relabel + skill edit), not mid-session invention. Personal mental model first; academic organization second when it does not fight the mental model.
_Avoid_: treating the ladder as frozen forever; inventing tags outside the closed list mid-session; forcing academic taxonomy over Juanes' model

**Spine / root tag**:
`#fundamentals` is the root of the scope ladder and the tag used only for root-level notes — cross-domain LEGO pieces with no honest narrower home. Always-load of spine words falls out of the normal parent walk to the root. It is not an extra mark stacked on domain notes.
_Avoid_: `#fundamentals` + `#swe` dual **scope** tags; treating fundamentals as orthogonal mastery flag; parking domain-specific words at the root just to force global load. (`#swe #weak` is fine — scope + understanding, not two homes.)

**Most-specific-only labeling**:
A note carries only its narrowest true scope tag, not parent tags. Parent expansion is the skill's job at retrieval. Optional `#weak` may sit beside the scope tag.
_Avoid_: full-path tags on every note

**Single-home rule**:
A note carries exactly one **scope** tag — the narrowest true home. If two homes feel equal: pick one, move one step broader to the shared parent, or split into two notes. An understanding tag is not a second home.
_Avoid_: multi-domain tagging, primary+secondary scope tags

**Weak status**:
When a `#weak` note is about to be used as an anchor or bare owned word, do not treat it as ground. Report it. `/teach` gates or routes around it. Membership listing alone is not use. A conversational gate does not clear the tag.
_Avoid_: using a weak body "with a caveat"; inline-patching past weak grip; clearing `#weak` for him; requiring a note rewrite before the session may stand on a just-gated concept

**Load set**:
Dictionary notes whose scope tag is in the **load tag set**.
- **Default branch:** detected narrowest relevant tag + every ancestor up to `#fundamentals`.
- **Extra scopes:** each is exact-tag only — notes literally tagged with that slug. No parent walk, no children. Widen later only if real use demands it.
This keeps connection-spotting cheap and avoids bloating context. Unknown extras that are not on the ladder and match no notes are reported, not silently ignored.

**Load payload**:
Default: filenames only (filtered license list). That answers "which owned words are in scope?" Full note bodies are opened only for words about to be used as anchors, or that Juanes explicitly names — not bulk-read for the whole load set.
_Avoid_: dumping every ancestor note body into context on every question

**Extra scope**:
A tag argument on skill invocation (example shape: dictionary load with `#economy`). Temporarily adds exact-tag notes for connection-spotting. Not written onto notes. Bottom-up: do not pre-design parent/child expansion for extras.

**Detected scope**:
The narrowest ladder tag that fits the current question or topic. Chosen by the agent from the closed ladder using the question's language; refined if Juanes names a tag explicitly.

## Scope ladder (working closed set)

Root:

- `#fundamentals`
  - `#engineering`
    - `#swe`
      - `#ai`
      - `#devops`
        - `#linux` (provisional; revisit from real use)
      - `#web_dev`
        - `#react`
        - `#javascript` (when a note needs it)
      - `#flutter` — under `#swe` directly, NOT under `#web_dev`
      - `#db`
  - `#math`
    - `#stats`

Ladder evolution: add/move/rename tags only when real notes or real questions create friction; update the skill's closed list and relabel affected notes in the same change.

False homes to reject: `#flutter` under `#web_dev`; long-form synonym tags; inventing thin roots (e.g. `#timezones`) when a broader home exists; stacking `#fundamentals` on domain notes for global load (use extra scopes or move the note to the root instead).

## Integrations (intent)

- `/teach` always invokes this skill's load protocol before teaching (no optional skip).
- Load payloads split **steady** vs **weak** members. Weak members stay on the filename list but are not safe anchors.
- `#weak` about to be used → report; `/teach` gates or routes around it. Dictionary does not teach.
- Manual/widened invocation accepts optional extra scope tags for connection-spotting.
