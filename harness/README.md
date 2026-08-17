# Harness — wiring the agents into a project

The harness is repo-portable: agent brains and history live in the harness checkout; this folder wires them into Claude Code.

## Install (per project repo, ~2 minutes)

1. Clone or copy `multi-agent-harness/` inside or beside the project repo.
2. Copy `harness/claude-config/` into the project repo **renamed to `.claude/`**:

   ```bash
   cp -r multi-agent-harness/harness/claude-config  project-repo/.claude
   ```

   (It ships as `claude-config/` rather than `.claude/` because dot-directories are write-protected in some environments and silently skipped by some copy tools.)

3. Install the G3 hook:

   ```bash
   sh multi-agent-harness/hooks/install-hooks.sh  /path/to/project-repo
   ```

4. Start a Claude Code session in the project repo. `/build` runs the loop, `/retro` closes the project, `/mechanic` runs the cadence audit.

If the harness lives somewhere non-standard, set `HARNESS_DIR` in your environment — the hook checks it first, then `<repo>/multi-agent-harness`, then `<repo>/../multi-agent-harness`, and refuses the commit rather than skipping the scan if it finds none.

## What's wired

- **`claude-config/agents/`** — six subagent definitions. Each is a thin shim that loads its binding brain from `agents/<name>/agent.md`, that agent's `memory/`, and the current model's adapter. The brains are the source of truth; shims stay thin so a brain edit takes effect everywhere at once.
- **`claude-config/commands/`** — `/build` (orchestrator: G0 → Scout → Builder → Verifier → Red-team → hard gates), `/retro` (Librarian close-out), `/mechanic` (cadence audit).
- **`checks/`** — gate scripts. `run_gates.py --pre-commit` runs the secret scan and hygiene lint; `--release` adds the placeholder lint (hard) and citation screen (advisory).
- **`hooks/pre-commit`** — G3 enforcement at commit time. Unwaivable; `--no-verify` is a SEV1 waiting to be filed.

## Independence rules (the part that's easy to break)

Verifier and Red-team must be dispatched **fresh**: spec, factsheet, and build package only. If the orchestrator pastes Builder's reasoning into their context, the fresh-context guarantee — the harness's core quality mechanism — is silently gone. The shims instruct those agents to detect and report contamination, but the orchestrator not causing it is the real control.

## Model switching

Set the model per agent role in your Claude Code configuration; the shims pick up the matching adapter from `adapters/`. Record `model` and `build_mode` in every artifact envelope — the improvement metrics are segmented by model and break silently without it.
