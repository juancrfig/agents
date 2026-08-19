---
name: get-feedback-fragment
description: "Generates a sanitized literal transcript of a conversation for later analysis and feedback."
---
# get-feedback-fragment

Log-only. Do not judge the fragment, the model, or the user. Do not fix the issue. Do not summarize, paraphrase, or rewrite message text or the Human Report except the sanitization substitutions below.

## When this runs

The user typed `/get-feedback-fragment` plus optional trailing text.

**Human Report** is a required field on every fragment. It is the user's statement of the error — what went wrong or what behavior to avoid. It is not left for later interpretation.

- Trailing text after `/get-feedback-fragment` **is** the Human Report. Copy it verbatim after sanitization. Do not treat it as instructions to analyze, and do not put it in the message list.
- If there is no trailing text, do not write a fragment. Ask once for the Human Report and wait. Do not invent, infer, or complete the report from the transcript.

## Fragment contents

Include, in order, the conversation span the command refers to:

1. The user message(s) that led to the unwanted result.
2. The assistant message(s) that were incorrect or unwanted.

If the span is ambiguous, use the immediately preceding user turn and the assistant turn it replies to. Do not add earlier turns "for context." Do not omit turns in that span. Do not include the slash-command turn in the message list.

Keep role labels (`user` / `assistant`). Keep tool-call names and error text if they appeared in those turns. Do not invent missing turns.

## Sanitize then write (do not rewrite)

Copy the selected messages and the Human Report token-for-token. The only allowed edits are replacing sensitive or environment-specific values with placeholders. Do not rephrase surrounding prose, code, or the report.

Replace every instance of a given value with the same placeholder in this fragment.

| Class | Placeholder |
| --- | --- |
| Secrets (tokens, passwords, API keys, cookies, auth headers, private keys) | `[SECRET]` |
| People names | `[NAME]` |
| Emails | `[EMAIL]` |
| Phone numbers | `[PHONE]` |
| Employer / customer / partner org names | `[ORG]` |
| Internal product, service, or codenames | `[PRODUCT]` |
| Absolute and user-specific paths; home directories | `[PATH]` |
| Hostnames, IPs, internal URLs | `[URL]` |
| Account, ticket, customer, and similar identifiers | `[ID]` |
| Unique repo, team, or project names that identify the workplace | `[PROJECT]` |

Leave generic programming language, public library names, and the Human Report wording intact. If unsure whether a token identifies a person, org, or workplace, replace it.

After substitution, the fragment must not contain recoverable secrets or workplace identity.

## Destination

Resolve grok home: `$GROK_HOME` if set, otherwise `~/.grok`.

Append one YAML document to:

`<grok-home>/feedback-fragments/log.yaml`

Create the directory and file if missing. Do not overwrite earlier documents.

Document shape (literal block scalars; keep newlines inside messages):

```yaml
---
captured_at: <ISO-8601 UTC>
human_report: |
  <sanitized Human Report>
messages:
  - role: user
    content: |
      <sanitized text>
  - role: assistant
    content: |
      <sanitized text>
```

Do not add fields for verdict, category, severity, or notes. Do not rewrite `human_report` into a "clearer" error statement.

## After writing

Reply with only the path written and how many messages were logged. No recap of the fragment or Human Report. No opinion on whether the model was wrong.