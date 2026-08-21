#!/usr/bin/env python3
"""Bootstrap the Hermes agent roster on a new machine.

Single entry point for provisioning from the agents repo (source of truth:
git@github.com:juancrfig/agents.git). Idempotent; safe to re-run.

What it does:
  1. default profile -> Router with display name "hermes" (the name `hermes`
     itself is reserved by the CLI, so the Router IS the default profile).
  2. creates mimir / horus / venus profiles, cloned from default.
  3. writes every profile's config.yaml: canonical_config.yaml base + role
     model + CLI toolsets + skills.disabled (installed bundle minus the
     manifest's per-agent list) + forced display settings that hide
     thinking (show_reasoning / interim_assistant_messages both false).
  4. copies avatars media/<name>.png -> <home>/assets/avatar.png (512 px).
  5. deploys manifest custom skills (repo skills/ -> <home>/skills/learning/).
  6. backfills the sdlc-review skill for the Router if missing (kanban
     review gate; environment-gated to kanban lanes).
  7. deploys the shared USER.md to every Hermes profile and the Router's
     canonical SOUL.md and MEMORY.md from repo hermes/.

Builder intentionally gets NO Hermes profile: it is the Grok Build & Codex
harnesses. The manifest still lists builder-skills for reference.

Usage:
  python3 bootstrap_roster.py [--repo PATH] [--dry-run] [--no-hermes]

  --repo PATH  agents repo location (default: ~/Projects/agents)
  --dry-run    print every command without executing
  --no-hermes  skip `hermes` CLI invocations (file operations only)
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML is required (hermes venv ships it)", file=sys.stderr)
    sys.exit(2)

DEFAULT_REPO = Path.home() / "Projects" / "agents"
HERMES_HOME = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
CONFIG_VERSION = 37

# Role models (source: README model tiers + nous provider catalog).
MODELS = {
    "hermes": "deepseek/deepseek-v4-flash",  # cheap, smart-enough, low latency
    "mimir": "deepseek/deepseek-v4-pro",     # mid-priced, smart teacher
    "horus": "google/gemini-3.7-flash",      # multimodal, agentic, latency-tolerant
    "venus": "openai/gpt-5.6-luna",          # strong multimodal reasoning
}

# Canonical CLI toolset (canonical_config.yaml) + per-role extras.
CLI_BASE = ["code_execution", "cronjob", "delegation", "file", "kanban", "memory",
            "session_search", "skills", "terminal", "vision", "web"]
CLI_EXTRAS = {
    "hermes": ["search", "computer_use"],
    "mimir": ["search"],
    "horus": ["search", "browser", "x_search"],
    "venus": ["search", "image_gen", "video_gen", "video"],
}

# Global kill-list shared by every profile (messaging/smart-home/misc).
COMMON_DISABLED = ["a2a", "bfl", "clarify", "context_engine", "desktop_ui",
                   "discord", "discord_admin", "feishu_doc", "feishu_drive",
                   "homeassistant", "spotify", "stt", "tts", "todo", "yuanbao"]

# Manifest section -> profile name (builder intentionally absent).
AGENTS = ["hermes", "mimir", "horus", "venus"]

PIC = {"hermes": "hermes.png", "mimir": "mimir.png",
       "horus": "horus.png", "venus": "venus.png"}


def log(msg):
    print(msg, flush=True)


def profile_home(name):
    """Profile home dir: the root home for default, profiles/<name> otherwise."""
    return HERMES_HOME if name == "default" else HERMES_HOME / "profiles" / name


def sh(cmd, dry):
    log(("[dry-run] " if dry else "$ ") + cmd)
    if dry:
        return 0
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        log(f"  ! exited {r.returncode}: {r.stdout.strip()} {r.stderr.strip()}")
    return r.returncode


def load_manifest(repo):
    m = yaml.safe_load((repo / "skills_manifest.yaml").read_text())
    out = {}
    for agent in AGENTS:
        sec = m.get(f"{agent}-skills", {})
        out[agent] = {
            "bundled": sec.get("bundled", []),
            "custom": sec.get("custom", []),
        }
    return out


def installed_skill_names(home):
    """Names of installed skills under a profile home's skills dir."""
    skills = home / "skills"
    if not skills.exists():
        return set()
    return {p.parent.name for p in skills.rglob("SKILL.md")}


def disabled_for(agent, spec, all_installed):
    enabled = set(spec["bundled"]) | set(spec["custom"])
    return sorted(all_installed - enabled)


def build_config(canonical, agent, spec, all_installed, cli_tools):
    cfg = dict(canonical)
    cfg["model"] = {"default": MODELS[agent], "provider": "nous",
                    "base_url": "https://inference-api.nousresearch.com/v1"}
    cfg["platform_toolsets"] = {"cli": cli_tools}
    cfg["agent"] = {"disabled_toolsets": list(COMMON_DISABLED)}
    cfg["skills"] = {"disabled": disabled_for(agent, spec, all_installed),
                     "write_approval": False}
    # Hiding thinking is part of the canonical display config; force it.
    cfg.setdefault("display", {})["show_reasoning"] = False
    cfg["display"]["interim_assistant_messages"] = False
    cfg["_config_version"] = CONFIG_VERSION
    return cfg


def write_config(home, cfg, dry):
    dest = home / "config.yaml"
    if dest.exists() and not dry:
        bak = dest.with_suffix(".yaml.bak")
        shutil.copy2(dest, bak)
        log(f"  backed up {dest} -> {bak}")
    body = yaml.safe_dump(cfg, sort_keys=False, default_flow_style=False,
                          allow_unicode=True)
    if dry:
        log(f"  [dry-run] would write {dest}")
    else:
        dest.write_text(body)
        log(f"  wrote {dest}")


def deploy_avatar(repo, agent, dry):
    home = profile_home("default" if agent == "hermes" else agent)
    src = repo / "media" / PIC[agent]
    dest = home / "assets" / "avatar.png"
    if dry:
        log(f"  [dry-run] would copy {src} -> {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS  # type: ignore[attr-defined]
        img = Image.open(src).convert("RGBA").resize((512, 512), resample)
        img.save(dest)
        log(f"  avatar {dest} (512px, PIL)")
    except ImportError:
        shutil.copy2(src, dest)
        log(f"  avatar {dest} (copied as-is, PIL not available)")


def deploy_custom_skills(repo, agent, spec, dry):
    home = profile_home("default" if agent == "hermes" else agent)
    for name in spec["custom"]:
        src = repo / "skills" / name
        if not (src / "SKILL.md").exists():
            log(f"  ! custom skill {name} missing in repo skills/ — skipped")
            continue
        dest = home / "skills" / "learning" / name
        if dry:
            log(f"  [dry-run] would copy {src} -> {dest}")
            continue
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        log(f"  custom skill {name} -> {dest}")


def deploy_context_files(repo, agent, dry):
    """Deploy shared user context and Router-specific soul/memory files."""
    home = profile_home("default" if agent == "hermes" else agent)
    copies = [(repo / "USER.md", home / "memories" / "USER.md")]
    if agent == "hermes":
        copies.extend([
            (repo / "hermes" / "SOUL.md", home / "SOUL.md"),
            (repo / "hermes" / "MEMORY.md", home / "memories" / "MEMORY.md"),
        ])
    for src, dest in copies:
        if dry:
            log(f"  [dry-run] would copy {src} -> {dest}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        log(f"  context {src.name} -> {dest}")


def ensure_sdlc_review(home, dry):
    """Backfill sdlc-review (kanban review gate) for the Router."""
    if "sdlc-review" in installed_skill_names(home):
        return
    if sh("hermes skills repair-official sdlc-review", dry) == 0:
        return
    # Fallback: copy from the upstream bundle source shipped with the install.
    candidates = [
        HERMES_HOME / "hermes-agent" / "skills" / "devops" / "sdlc-review",
        Path(sys.prefix) / "skills" / "devops" / "sdlc-review",
    ]
    for cand in candidates:
        if (cand / "SKILL.md").exists():
            dest = home / "skills" / "devops" / "sdlc-review"
            if dry:
                log(f"  [dry-run] would copy {cand} -> {dest}")
                return
            shutil.copytree(cand, dest)
            log(f"  sdlc-review backfilled from upstream bundle -> {dest}")
            return
    log("  ! sdlc-review not found; repair-official failed and no upstream "
        "bundle path matched. Install manually (kanban review gate).")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=str(DEFAULT_REPO))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-hermes", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo).expanduser()
    for required in ("canonical_config.yaml", "skills_manifest.yaml", "media",
                     "USER.md", "hermes/SOUL.md", "hermes/MEMORY.md"):
        if not (repo / required).exists():
            print(f"error: agents repo not found at {repo} (missing {required})",
                  file=sys.stderr)
            sys.exit(1)

    dry = args.dry_run
    manifest = load_manifest(repo)
    canonical = yaml.safe_load((repo / "canonical_config.yaml").read_text())
    log(f"repo: {repo}\nhermes home: {HERMES_HOME}\n")

    # 1. Default profile = Router, display name "hermes".
    if not args.no_hermes:
        sh("hermes profile rename default hermes", dry)

    # 2. Create missing profiles, cloned from default (inherits .env keys).
    for agent in ["mimir", "horus", "venus"]:
        if (HERMES_HOME / "profiles" / agent / "config.yaml").exists() and not dry:
            log(f"profile {agent} exists — skipping create")
            continue
        desc = {
            "mimir": "Teacher: explains concepts tailored to Juanes' learning style. Runs /teach + dictionary load protocol.",
            "horus": "Scout: strategic internet research, curated source-cited reports. Multimodal retrieval.",
            "venus": "Graphic designer: image/video generation and editing, artistic design, art direction.",
        }[agent]
        sh(f'hermes profile create {agent} --clone --description "{desc}"', dry)

    # 3-6. Configs, avatars, custom skills, sdlc-review — per agent.
    all_installed = set()
    for agent in AGENTS:
        home = profile_home("default" if agent == "hermes" else agent)
        all_installed |= installed_skill_names(home)
    # Include manifest names even if not yet installed (robust disabled set).
    for agent in AGENTS:
        all_installed |= set(manifest[agent]["bundled"]) | set(manifest[agent]["custom"])

    for agent in AGENTS:
        log(f"== {agent} ==")
        spec = manifest[agent]
        home = profile_home("default" if agent == "hermes" else agent)
        cli = list(CLI_BASE) + CLI_EXTRAS[agent]
        cfg = build_config(canonical, agent, spec, all_installed, cli)
        write_config(home, cfg, dry)
        deploy_avatar(repo, agent, dry)
        deploy_custom_skills(repo, agent, spec, dry)
        deploy_context_files(repo, agent, dry)
        if agent == "hermes":
            ensure_sdlc_review(home, dry)

    log("\nNext: verify (see SKILL.md #Verification):")
    log("  hermes profile list")
    log("  hermes -p <name> skills list   (enabled counts per manifest)")
    log("  ls <home>/assets/avatar.png    (one per profile)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
