# Daily Codex Results Site Design

## Goal

Build a GitHub repository that receives results from multiple Codex automations and renders those results as a daily HTML dashboard with history through GitHub Pages.

## Architecture

Automations do not edit HTML directly. Each automation writes one structured JSON result into `runs/YYYY-MM-DD/`. A deterministic Node.js generator reads all results and rebuilds the static site in `public/`.

This keeps concurrent automations simple: they only own their result file. The generated dashboard owns today's view, history pages, per-day pages, and per-task pages.

## Components

- `AUTOMATION_CONTRACT.md`: durable instructions for future Codex automations.
- `AGENTS.md`: short repository-level rules for Codex.
- `runs/`: source-of-truth result records.
- `scripts/build-site.mjs`: validates and renders the static site.
- `scripts/build-site.test.mjs`: tests validation and generation behavior.
- `public/`: generated GitHub Pages output.
- `.github/workflows/pages.yml`: deploys `public/` through GitHub Pages.

## Data Flow

1. A Codex automation completes work.
2. It writes `runs/YYYY-MM-DD/<task-id>.json`.
3. It runs `npm run build`.
4. The generator validates all JSON results and rebuilds `public/`.
5. GitHub Pages deploys `public/` after the commit reaches `main`.

## Error Handling

The generator fails fast when required fields are missing, status is unknown, the date folder is invalid, or timestamps are malformed. This makes automation failures visible before broken HTML is committed.

## Testing

Use Node's built-in test runner. Tests cover result validation, result collection, and generation of root, day, task, and machine-readable data pages.

