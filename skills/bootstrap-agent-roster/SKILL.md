---
name: bootstrap-agent-roster
description: Bootstrap the full agent roster on a new machine.
version: 0.1.0
author: Hermes
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Bootstrap, Roster, Profiles, Provisioning]
---

# Bootstrap Agent Roster

Provision a fresh Hermes install with Juanes' full agent roster from the agents repo (`git@github.com:juancrfig/agents.git`): the default profile becomes the Router with display name `hermes`, plus `mimir` (Teacher), `horus` (Scout), and `venus` (Artist) profiles — each with the canonical config, role model, trimmed skill set, avatar, custom skills, and shared `USER.md`. The Router also receives its canonical `SOUL.md` and `MEMORY.md`. Builder intentionally gets NO Hermes profile (it is the Grok Build & Codex harnesses). This skill does NOT install Hermes, log into providers, or configure messaging gateways.

## When to Use

- Setting up a new machine or fresh Hermes install for the roster
- Re-syncing profile configs, avatars, or custom skills after repo changes
- Checking the roster state with `--dry-run` before touching anything

## Prerequisites

- Agents repo cloned: `git clone git@github.com:juancrfig/agents.git ~/Projects/agents`
- Hermes installed and authenticated (nous portal login done) — profiles are cloned from default to inherit `.env` keys
- Python 3 with PyYAML (hermes venv ships it); Pillow optional (avatar downscale; falls back to plain copy)
- Repo `skills/` is the source of truth for custom skills; the manifest currently deploys `teach` and `vocabulary` to Mimir plus this bootstrap skill to the Router.

## How to Run

Invoke through the `terminal` tool:

```bash
python3 ~/Projects/agents/skills/bootstrap-agent-roster/scripts/bootstrap_roster.py [--repo PATH] [--dry-run] [--no-hermes]
```

- `--dry-run` prints every command without executing (review before running).
- `--no-hermes` skips `hermes` CLI calls (file operations only).

## Quick Reference

| Agent | Profile | Model | Avatar | Custom skills deployed |
|---|---|---|---|---|
| Router | default (display name `hermes`) | `deepseek/deepseek-v4-flash` | `media/hermes.png` | `bootstrap-agent-roster` |
| Teacher | `mimir` | `deepseek/deepseek-v4-pro` | `media/mimir.png` | `teach`, `vocabulary` |
| Scout | `horus` | `google/gemini-3.7-flash` | `media/horus.png` | — |
| Artist | `venus` | `openai/gpt-5.6-luna` | `media/venus.png` | — |
| Builder | none (external harnesses) | — | `media/builder.png` (manifest only) | — |

Skill counts per agent: hermes 18 per manifest but **17 visible** in `skills list` (sdlc-review is kanban-gated and never lists), mimir 13 (11 bundled + 2 custom), horus 15, venus 16, builder 9 (manifest only). Source: `skills_manifest.yaml`.

## Procedure

1. Clone the repo and confirm prerequisites.
2. Preview: `python3 .../bootstrap_roster.py --dry-run` — the script reads `canonical_config.yaml` + `skills_manifest.yaml` and prints every command.
3. Run: `python3 .../bootstrap_roster.py`. It is idempotent — re-running re-applies configs/avatars/skills without duplicating profiles.
4. What the script does, in order:
   - `hermes profile rename default hermes` — Router display name (the name `hermes` is reserved by the CLI; the Router IS the default profile).
   - `hermes profile create <name> --clone --description "<role>"` for mimir, horus, venus (skipped when they exist).
   - Writes each profile's `config.yaml`: canonical base + role model + CLI toolsets + `skills.disabled` (installed bundle minus the manifest list) + `display.show_reasoning: false` / `display.interim_assistant_messages: false` (hiding thinking) + `skills.write_approval: false`. Existing configs get a `.bak` copy.
   - Copies `media/<name>.png` → `<home>/assets/avatar.png`, downscaled to 512 px.
   - Copies manifest custom skills from repo `skills/` → `<home>/skills/learning/`.
   - Copies root `USER.md` into every profile's memory store; copies `hermes/SOUL.md` and `hermes/MEMORY.md` into the Router.
   - Backfills `sdlc-review` for the Router (kanban review gate) via `hermes skills repair-official`, falling back to the upstream bundle source.
5. Commit nothing on the new machine — the repo is only read; all writes land in `~/.hermes`.

## Pitfalls

- `hermes` profile name is reserved — never `hermes profile create hermes`. The Router is the default profile, display name set via rename.
- **Re-running bootstrap OVERWRITES every profile's `config.yaml` from `canonical_config.yaml`** — it carries over only `model`, `platform_toolsets`, `skills.disabled`, `agent.disabled_toolsets`, and display overrides. Anything else added locally to a profile config since the last run is DROPPED (e.g. the Router's `platforms.telegram.enabled: true` got wiped on 2026-08-19, taking the Telegram gateway down with it). The old config is preserved as `config.yaml.bak` — restore with `cp <home>/config.yaml.bak <home>/config.yaml` then restart the gateway, or re-apply the dropped keys. Before running, diff current profile configs against the canonical output (`--dry-run` shows the plan but not the diff) and re-apply local keys afterward.
- A mid-session bootstrap run also DISABLES skills in the current profile (they vanish from `skills list` if not in the manifest's enabled lists) — expect the currently-loaded skill itself to become unloadable afterward.
- Builder has no Hermes profile by design (Grok Build & Codex harnesses); do not create one.
- `sdlc-review` is environment-gated (frontmatter `environments: [kanban]`) — it never appears in a normal `skills list`; that is expected, not a failure.
- The Router's avatar copy overwrites `~/.hermes/assets/avatar.png` — a pre-existing default avatar is replaced (back it up if it is precious).
- Custom skills are COPIED, not symlinked — after editing a skill in the repo, re-run the script to redeploy.
- `hermes update` re-seeds bundled skills; the per-profile `skills.disabled` list keeps the visible set at the manifest's list. A `.no-bundled-skills` marker in a home opts it out of seeding entirely.
- On a fresh machine, run provider auth (`hermes setup` / portal login) BEFORE the script, so the profile clones carry working `.env` keys.

## Verification

```bash
hermes profile list                                   # hermes (default) + mimir/horus/venus
hermes -p <name> skills list | grep -c '│ enabled '   # hermes 17 visible, mimir 14, horus 15, venus 16
ls ~/.hermes/assets/avatar.png ~/.hermes/profiles/{mimir,horus,venus}/assets/avatar.png
ls ~/.hermes/skills/devops/sdlc-review/SKILL.md        # kanban-gated: present but never lists
python3 -c "import yaml;c=yaml.safe_load(open('$HOME/.hermes/profiles/mimir/config.yaml'));print(c['display'])"
```

The last check must print `show_reasoning: False` and `interim_assistant_messages: False` (hiding thinking applied to all profiles).
