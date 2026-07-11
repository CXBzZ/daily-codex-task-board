# Task 1 Report: Model Auto-Discovered Agent Boards

## Status

DONE

## Implementation

- Added `RESERVED_AGENT_IDS` with the reserved IDs `codex` and `workbuddy`.
- Updated required external-agent normalization to reject a slugified reserved ID with the specified error.
- Added `agentName` and `agentRole` metadata to the built-in Codex and WorkBuddy boards, with each board title set to its agent name.
- Added `createDiscoveredAgentBoards(runs)`, which groups normalized runs by `agentId`, derives isolated board paths and metadata, and sorts boards by display name.
- Preserved the existing internal `AGENTS_BOARD` build path for compatibility; no Task 2 routing or UI work was added.

## Files Changed

- `scripts/build-site.mjs`
- `scripts/build-site.test.mjs`
- `.superpowers/sdd/task-1-report.md`

## TDD Evidence

### RED

Command:

```text
node --test --test-name-pattern="reserved id|groups agents" scripts/build-site.test.mjs
```

Result: failed as expected during module loading because `RESERVED_AGENT_IDS` was not exported yet. The focused test could not import the requested new API, confirming the feature was missing before implementation.

### GREEN

Focused command:

```text
node --test --test-name-pattern="reserved id|groups agents" scripts/build-site.test.mjs
```

Result: 2 tests passed, 0 failed.

Full command:

```text
npm test
```

Result: 14 tests passed, 0 failed, 0 skipped, 0 cancelled.

Additional check:

```text
git diff --check
```

Result: passed with no whitespace errors.

## Self-Review

- The reserved-ID check is gated by `requireAgent`, so built-in Codex and WorkBuddy records remain compatible with their existing source directories.
- Discovery consumes normalized, already-descending runs, so the first run in each group supplies the latest agent metadata as required.
- Board routes include the agent ID, preventing task-path collisions between agents.
- Existing mixed-agent generation remains available internally, satisfying the sequencing constraint.
- No generation routing, navigation, or UI changes were introduced.

## Concerns

No known concerns for Task 1. The new discovery model is intentionally not wired into `buildSite` until the later routing task.
