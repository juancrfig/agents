---
name: research
description: "Run reliable, criteria-based investigations of external or internet claims. Use this whenever a question is material, current, disputed, high-stakes, publishable, durable, explicitly evidence-requested, or unresolved; escalate when uncertain."
version: 1.0.0
author: Operations Module
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, evidence, scientific-method, citations, verification]
    category: research
---

# Research protocol

Use this skill for empirical claims. It is the epistemic protocol, not a worker
scheduler. Keep judgement, grading, contradiction handling, conclusion, and the
user-facing report in the main session.

## Activation and tracks

Use **full protocol** for material/current/disputed/high-stakes/publishable,
durable, explicitly evidence-requested, or unresolved claims. Use **lightweight
retrieval** for incidental syntax/version lookups, routine local checks, and stable
low-stakes facts. When uncertain, use full protocol. If ambiguity could change the
method or conclusion, grill the user in the main session; never delegate, batch,
cron, or simulate that grill.

For a local/system fact, `I ran the check I could run` is a finding when the check
is recorded. Do not perform the full ceremony for that fact. Do not A–U-grade
normative or value claims; separate their empirical premises from values,
constraints, risk tolerance, and trade-offs.

## Full execution order

1. **Classify and specify.** State the question, claim units, scope, definitions,
   geography/population, temporal boundary, exclusions, and what would settle it.
2. **Record the initial prior.** Capture the prior before inspecting the wiki,
   prior sessions, or new evidence. State assumptions and expected disconfirmation.
3. **Check memory stores.** Inspect the PI wiki and relevant prior sessions. Treat
   them as leads/cache, never as fresh evidence; re-retrieve load-bearing sources.
4. **Declare method and budget.** Name the method, source classes, query families,
   time/tool budget, and stopping rule. Match method to claim (descriptive,
   causal, predictive, comparative, or normative).
5. **Open a fresh citation ledger.** Use `grounded-citations`; register each URL
   at retrieval time, before drafting. Example:
   ```bash
   S="${HERMES_HOME:-$HOME/.hermes}/.agent-sync/skills-projection/canonical-skills/research/grounded-citations/scripts/sources.py"
   python3 "$S" reset
   python3 "$S" add <url> --title "<title>"
   python3 "$S" quote <id> --text "<verbatim text>" --from <fetched-text>
   python3 "$S" verify <draft> --strict --evidence
   ```
   Use `--ledger <path>` or `HERMES_CITATION_LEDGER` when a task needs an
   explicit ledger path. Never invent IDs or reconstruct URLs from memory.
6. **Observe.** Retrieve and preserve source text, URLs/post IDs, timestamps, and
   failures. A search snippet is not page evidence. For X, preserve handle,
   post ID/URL, post timestamp, retrieval timestamp, author context, and the
   exact post text; distinguish a post from a claim about a post.
7. **Analyze claim by claim.** Build a source card for every load-bearing source:
   `source_id`, URL/post ID, origin chain (underlying document/data/event),
   source class, directness, provenance, method visibility, freshness relative
   to the declared temporal boundary, incentives/conflicts, scope match, exact
   quote/observation, and retrieval date. Trace independence to materially
   separate underlying origins; different publishers or mirrors are not
   independent when they repeat one origin.
8. **Falsify.** For every material empirical claim, run at least one explicit
   counterclaim query family and one source-appropriate disconfirmation route.
   High-stakes, disputed, or A-grade claims require two independent counterclaim
   routes, or a recorded reason one was impossible.
9. **Resolve contradictions.** Surface both readings with source cards. Differences
   explained by time, geography, population, or definitions are scope differences,
   not necessarily contradictions. An unresolved material contradiction between
   acceptable sources for the same scope/time prevents A and B; grade D/contested
   until reconciled.
10. **Grade and conclude.** Apply the rubric below to each empirical claim, then
    grade the conclusion as the minimum grade of every load-bearing empirical claim.
11. **Report and file.** Render citations mechanically, state failures/exclusions,
    and record the wiki action. The durable record is the evidence record, not a
    pointer to a mutable cache.

## Criteria-based support rubric

Use exactly one grade per empirical claim. Grade is the weakest applicable
condition, never an average or an intuition.

| Grade | Gate (all conditions in the row) | Label |
|---|---|---|
| **A** | At least 2 materially independent sources; at least 1 primary/direct observation; exact scope/time match; inspectable provenance and method; verified verbatim text for external sources; no unresolved material contradiction | `finding` |
| **B** | 1 strong primary/direct source plus 1 materially independent corroboration; stated limitations; verified quote/observation; no unresolved material contradiction | `finding` |
| **C** | One acceptable quoted/observed source, or secondary-only/incomplete/insufficiently independent evidence | `inference` |
| **D** | Contested, stale beyond the declared boundary, tertiary/social-only, anonymous/context-poor, or materially contradicted evidence | `guess` or `contested` |
| **U** | Adequate evidence was not located, accessed, or verified; record the search/access failure and what would settle it | `unverified` |

Classify sources as **primary** (the thing itself: official record, paper,
repo, statute, dataset, live system, direct post, or direct observation),
**secondary** (reporting on a primary), or **tertiary** (roundup, SEO, or
unsourced social summary). A source without verifiable text cannot independently
support an A/B external finding; record the failure and downgrade it to lead,
context, C, D, or U as applicable.

Causal claims require a named, defensible identification strategy (for example,
randomization, natural experiment, difference-in-differences, instrumental
variable, regression discontinuity, or a clearly justified design). Without one,
a causal claim cannot exceed **C**. Predictions record horizon, assumptions,
reference class/base rate when available, falsifier, source basis, and a future
verification trigger.

## Terminal states and done gate

- `done`: all applicable gates pass within declared scope.
- `unverified`: evidence was insufficient or could not be verified.
- `blocked`: a required source, tool, permission, or action prevented completion.
- `abandoned`: the user or an explicit resource boundary stopped the investigation.

Every non-`done` result names remaining work, the blocker/boundary, and what would
change the state. Before declaring `done`, verify: scope/method/prior are recorded;
claims are separated and labeled; every source is registered with a source card;
required quotes pass the quote gate; counterclaims and contradictions were checked;
grades obey the table and causal cap; no claim exceeds source scope; conclusion grade
is the weakest load-bearing grade; citations verify; uncertainty/failures are stated;
and wiki filing or deliberate non-filing is recorded.

## Report contract

Return: **status**, question/scope/method, initial prior, key claims with grade and
label, source cards/citations, counterclaims, contradictions and resolution,
conclusion with weakest-link grade, limitations/failures, stopping reason, and wiki
action. For lightweight retrieval, answer directly and say what check/retrieval was
performed; do not manufacture a full report.

## Worker-neutral interface

Workers, if used, may perform only bounded observation: search a declared query set,
fetch named URLs, extract text, or scan a declared corpus. Their result is an input,
never a finding, grade, conclusion, or done-state. The main session owns the question,
method, source classes, ledger policy, source-card review, counterclaims,
contradictions, grades, conclusion, wiki decision, and every word to the user.
Worker count/concurrency, model, authority, output schema, persistence, retries,
escalation, and parent re-fetch policy are intentionally deferred to the separate
swarm grill; do not invent those policies here.

## Privacy and reproducibility

Do not place credentials, private data, or unnecessary personal information in
source cards or durable records. Preserve retrieval dates, query families, source
failures, exclusions, ledger, quotes, post IDs, assumptions, and stopping reason so
another investigator can reproduce the result within the declared scope.

Do not confuse a cached wiki answer, a worker self-report, a fluent explanation, or
an uncited search snippet with verified evidence.
