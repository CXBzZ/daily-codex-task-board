# Daily Codex Results Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a static GitHub Pages dashboard that aggregates Codex automation result JSON files into today's view and historical HTML pages.

**Architecture:** Codex automations write JSON files under `runs/YYYY-MM-DD/`. A zero-dependency Node.js generator validates those results and rebuilds `public/`, while GitHub Actions deploys the generated directory.

**Tech Stack:** Node.js 20+, Node built-in test runner, GitHub Actions, GitHub Pages static hosting.

---

### Task 1: Repository Contract And Documentation

**Files:**
- Create: `AUTOMATION_CONTRACT.md`
- Create: `AGENTS.md`
- Create: `README.md`
- Create: `.gitignore`
- Create: `package.json`

- [x] Define the shared result contract with required fields, optional fields, file naming, and automation prompt template.
- [x] Add repository-level Codex rules that point automations at the contract.
- [x] Add user-facing README instructions and npm scripts.
- [x] Ignore local machine, dependency, environment, and worktree files.

### Task 2: Static Site Generator

**Files:**
- Create: `scripts/build-site.mjs`

- [x] Implement result collection from `runs/YYYY-MM-DD/*.json`.
- [x] Validate task id, task name, status, summary, date folder, optional timestamps, labels, next steps, and artifacts.
- [x] Normalize result records into a stable shape for rendering.
- [x] Generate `public/index.html`, `public/history.html`, `public/days/*.html`, `public/tasks/*.html`, `public/assets/styles.css`, and `public/data/runs.json`.

### Task 3: Tests And Sample Data

**Files:**
- Create: `scripts/build-site.test.mjs`
- Create: `runs/2026-07-05/example-codex-task.json`

- [x] Test timezone date formatting.
- [x] Test result collection and normalization.
- [x] Test that site generation writes root, day, task, and data files.
- [x] Add a sample automation result so the initial site is not blank.

### Task 4: GitHub Pages Workflow

**Files:**
- Create: `.github/workflows/pages.yml`

- [x] Run tests and build on pushes to `main`.
- [x] Upload `public/` as a Pages artifact.
- [x] Deploy to GitHub Pages with the official deploy action.

### Task 5: Verification

**Files:**
- Generated: `public/**`

- [ ] Run `npm test`.
- [ ] Run `npm run build`.
- [ ] Inspect generated files.
- [ ] Check git status before reporting completion.

