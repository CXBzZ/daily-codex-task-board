# Repository Instructions

This repository is a static dashboard for automation results from multiple sources (Codex and WorkBuddy).

## Codex Automations

When you are a Codex automation working in this repository:

- Read `AUTOMATION_CONTRACT.md` before writing results.
- Write result JSON files under `runs/YYYY-MM-DD/`.
- Do not edit `public/` manually.
- Run `npm run build` after changing files in `runs/`.
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

