# Repository Instructions

This repository is a static dashboard for automation results from multiple sources (Codex and WorkBuddy).

## Codex Automations

When you are a Codex automation working in this repository:

- Read `AUTOMATION_CONTRACT.md` before writing results.
- Write primary Codex result JSON files under `runs/YYYY-MM-DD/`.
- Write WorkBuddy result JSON files under `runs-workbuddy/YYYY-MM-DD/` after reading `WORKBUDDY_CONTRACT.md`.
- Write other personal assistant agent result JSON files under `runs-agents/YYYY-MM-DD/` only after reading `AGENT_ONBOARDING.md` and `AGENT_BOARD_CONTRACT.md`.
- Do not edit `public/` manually.
- Run `npm run build` after changing files in `runs/`, `runs-workbuddy/`, or `runs-agents/`.
- Run `npm test` after changing scripts or the result contract.
- Keep generated HTML and source JSON in the same commit.

## WorkBuddy Automations

When you are a WorkBuddy automation working in this repository:

- Read `WORKBUDDY_CONTRACT.md` before writing results.
- Write result JSON files under `runs-workbuddy/YYYY-MM-DD/` (not `runs/`).
- Do not edit `public/` manually.
- Run `npm run build` after changing files in `runs-workbuddy/`.
- Run `npm test` after changing scripts or the result contract.
- Keep generated HTML and source JSON in the same commit.

Both pipelines share the same JSON schema but use separate directories. Do not write WorkBuddy results into `runs/` or Codex results into `runs-workbuddy/`.

## External Personal Assistant Agents

When you are a personal assistant agent that is not a built-in Codex or WorkBuddy automation:

- Read `AGENT_ONBOARDING.md` before your first result and `AGENT_BOARD_CONTRACT.md` before writing any result JSON.
- Write results under `runs-agents/YYYY-MM-DD/` using a stable external `agentId`; do not use the reserved IDs `codex` or `workbuddy`.
- Do not edit `public/` manually. Run `npm run build` and commit the source JSON with generated `public/` files.
