# Multi-Agent Task Board Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Replace the mixed personal-agent page with automatically discovered, isolated Agent tabs that each show today's results and their own history.

**Architecture:** Keep the Node.js static generator and existing result directories. Convert every source into a board context, group runs-agents records by agentId, and render all boards through one route-aware pipeline. Vertical tabs remain plain links, so every home, date, and task page is static and deep-linkable.

**Tech Stack:** Node.js 20+, ES modules, node:test, generated HTML/CSS, GitHub Pages.

## Global Constraints

- Codex reads runs/YYYY-MM-DD/ and WorkBuddy reads runs-workbuddy/YYYY-MM-DD/.
- External agents write runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json with agentId and agentName.
- External IDs codex and workbuddy are reserved.
- Codex and WorkBuddy are pinned first; discovered agents sort by display name.
- Every Agent home contains Today and History.
- External routes include agentId, isolating identical task IDs.
- Existing Codex and WorkBuddy URLs stay valid.
- public/ is generated only by npm run build; source JSON and generated HTML stay together.
- Add no runtime dependencies.

## File Map

- Modify scripts/build-site.mjs: discovery, routing, rendering, redirects, and CSS.
- Modify scripts/build-site.test.mjs: discovery, isolation, navigation, history, and compatibility tests.
- Create AGENT_ONBOARDING.md: quick-start instructions for future agents.
- Modify AGENT_BOARD_CONTRACT.md, README.md, and AGENTS.md: align repository guidance.
- Regenerate public/: publish the new static layout.

---

### Task 1: Model Auto-Discovered Agent Boards

**Files:**
- Modify: scripts/build-site.test.mjs
- Modify: scripts/build-site.mjs

**Interfaces:**
- Consumes: normalized records returned by collectRuns().
- Produces: RESERVED_AGENT_IDS and createDiscoveredAgentBoards(runs), returning Array<{ board, runs }>.

- [ ] **Step 1: Write failing validation and grouping tests**

Update the test imports to include RESERVED_AGENT_IDS and createDiscoveredAgentBoards, remove AGENTS_BOARD, and add:

~~~js
test("normalizeRun rejects external agents that use a reserved id", () => {
  const filePath = path.join(os.tmpdir(), "runs-agents", "2026-07-05", "codex--review.json");
  assert.throws(
    () => normalizeRun({
      agentId: "codex",
      agentName: "Not Codex",
      taskId: "daily-review",
      taskName: "Daily Review",
      status: "success",
      summary: "Review completed."
    }, filePath, path.join(os.tmpdir()), { requireAgent: true }),
    /reserved agentId "codex"/
  );
  assert.deepEqual([...RESERVED_AGENT_IDS], ["codex", "workbuddy"]);
});

test("createDiscoveredAgentBoards groups agents and sorts by display name", () => {
  const contexts = createDiscoveredAgentBoards([
    { agentId: "zeta", agentName: "Zeta Agent", agentRole: "Operations", taskId: "review", date: "2026-07-05" },
    { agentId: "alice", agentName: "Alice Agent", agentRole: "Research", taskId: "review", date: "2026-07-05" }
  ]);

  assert.deepEqual(contexts.map(({ board }) => board.key), ["alice", "zeta"]);
  assert.equal(contexts[0].board.indexFile, "agents/alice/index.html");
  assert.equal(contexts[0].board.dayDir, "agents/alice/days");
  assert.equal(contexts[0].board.taskDir, "agents/alice/tasks");
  assert.equal(contexts[0].board.dataFile, "agents/alice.json");
});
~~~

- [ ] **Step 2: Run the focused test and verify RED**

Run:

    node --test --test-name-pattern="reserved id|groups agents" scripts/build-site.test.mjs

Expected: FAIL because both exports are missing and reserved IDs are accepted.

- [ ] **Step 3: Implement validation and discovery**

Add:

~~~js
export const RESERVED_AGENT_IDS = new Set(["codex", "workbuddy"]);
~~~

Add agentName and agentRole to CODEX_BOARD and WORKBUDDY_BOARD. Set each title to its Agent name. After slugifying an external ID, reject a reserved value:

~~~js
const agentId = slugifyTaskId(value);
if (options.requireAgent && RESERVED_AGENT_IDS.has(agentId)) {
  throw new Error(filePath + ': reserved agentId "' + agentId + '" cannot be used in runs-agents.');
}
return agentId;
~~~

Add this complete function after groupBy():

~~~js
export function createDiscoveredAgentBoards(runs) {
  return [...groupBy(runs, (run) => run.agentId).entries()]
    .map(([agentId, agentRuns]) => {
      const latest = agentRuns[0];
      const agentName = latest.agentName;
      const agentRole = latest.agentRole || "Personal assistant agent";
      const prefix = "agents/" + agentId;

      return {
        board: {
          key: agentId,
          agentName,
          agentRole,
          sourceLabel: agentName,
          eyebrow: "Personal Agent",
          title: agentName,
          lede: latest.agentRole || "Daily automation results and historical outcomes.",
          dayDir: prefix + "/days",
          taskDir: prefix + "/tasks",
          indexFile: prefix + "/index.html",
          historyFile: null,
          dataFile: "agents/" + agentId + ".json",
          historyEyebrow: agentName + " History",
          historyTitle: "All recorded " + agentName + " days",
          dayEyebrow: agentName + " Day",
          taskEyebrow: agentName + " Task",
          emptyMessage: "No " + agentName + " automation results have been reported for today yet.",
          historyEmptyMessage: "No " + agentName + " history has been generated yet."
        },
        runs: agentRuns
      };
    })
    .sort((left, right) => left.board.agentName.localeCompare(right.board.agentName));
}
~~~

- [ ] **Step 4: Verify GREEN and commit**

Run the focused command again and npm test. Remove the obsolete test comparing AGENTS_BOARD paths.

    git add scripts/build-site.mjs scripts/build-site.test.mjs
    git commit -m "refactor: model independent agent boards"

---

### Task 2: Generate Isolated Per-Agent Routes And Feeds

**Files:**
- Modify: scripts/build-site.test.mjs
- Modify: scripts/build-site.mjs

**Interfaces:**
- Consumes: built-in board constants and discovered { board, runs } entries.
- Produces: route-aware board contexts, isolated HTML, data/agents/<agent-id>.json, and agentCount.
- Preserves: data/agent-runs.json plus built-in feeds and URLs.

- [ ] **Step 1: Write a failing integration test**

Add this complete test:

~~~js
test("buildSite isolates agents with matching task ids", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "agent-isolation-"));
  const runsDir = path.join(tempDir, "runs");
  const agentsRunsDir = path.join(tempDir, "runs-agents");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(agentsRunsDir, "2026-07-05", "alice--review.json"), {
    agentId: "alice",
    agentName: "Alice Agent",
    agentRole: "Research",
    taskId: "daily-review",
    taskName: "Daily Review",
    status: "success",
    summary: "Alice result."
  });
  await writeJson(path.join(agentsRunsDir, "2026-07-05", "bob--review.json"), {
    agentId: "bob",
    agentName: "Bob Agent",
    agentRole: "Operations",
    taskId: "daily-review",
    taskName: "Daily Review",
    status: "needs_attention",
    summary: "Bob result."
  });

  const result = await buildSite({
    runsDir,
    agentsRunsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  assert.equal(result.agentCount, 2);
  await assertFileContains(path.join(outDir, "agents", "alice", "index.html"), "Alice result.");
  await assertFileContains(path.join(outDir, "agents", "alice", "tasks", "daily-review.html"), "Alice result.");
  await assertFileContains(path.join(outDir, "agents", "bob", "tasks", "daily-review.html"), "Bob result.");
  await assertFileContains(path.join(outDir, "data", "agents", "alice.json"), "Alice result.");

  const aliceTask = await fs.readFile(
    path.join(outDir, "agents", "alice", "tasks", "daily-review.html"),
    "utf8"
  );
  const aliceFeed = await fs.readFile(path.join(outDir, "data", "agents", "alice.json"), "utf8");
  assert.ok(!aliceTask.includes("Bob result."));
  assert.ok(!aliceFeed.includes("Bob result."));
  await assertFileContains(path.join(outDir, "data", "agent-runs.json"), "Bob result.");
});
~~~

- [ ] **Step 2: Run it and verify RED**

    node --test --test-name-pattern="matching task ids" scripts/build-site.test.mjs

Expected: FAIL because only the mixed Agent board exists.

- [ ] **Step 3: Add context, feed, and base helpers**

~~~js
function createBoardContext(board, runs) {
  return {
    board,
    runs,
    groupedByDay: groupBy(runs, (run) => run.date),
    groupedByTask: groupBy(runs, (run) => run.taskId)
  };
}

async function writeJsonFeed(outDir, dataFile, payload) {
  const filePath = path.join(outDir, "data", dataFile);
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(payload, null, 2) + os.EOL, "utf8");
}

function rootBase(fileName) {
  return "../".repeat(fileName.split("/").length - 1);
}
~~~

- [ ] **Step 4: Render ordered contexts**

Inside buildSite(), create contexts in this order:

~~~js
const discoveredBoards = createDiscoveredAgentBoards(agentRuns);
const contexts = [
  createBoardContext(CODEX_BOARD, codexRuns),
  createBoardContext(WORKBUDDY_BOARD, workbuddyRuns),
  ...discoveredBoards.map(({ board, runs }) => createBoardContext(board, runs))
];
const boards = contexts.map(({ board }) => board);

for (const context of contexts) {
  await renderBoardPages({ ...context, boards, outDir, today, generatedAt, timeZone });
}
~~~

Write all feeds through writeJsonFeed(). Return agentCount and sum discovered context day/task counts independently.

Update renderBoardPages() to create nested parent directories, skip null historyFile, and pass boards plus rootBase(fileName) to every renderer. All day/task links must start with base before board.dayDir or board.taskDir.

- [ ] **Step 5: Verify GREEN and commit**

    node --test --test-name-pattern="matching task ids" scripts/build-site.test.mjs
    npm test
    git add scripts/build-site.mjs scripts/build-site.test.mjs
    git commit -m "feat: generate isolated agent pages"

---

### Task 3: Render Vertical Agent Tabs With Today And History

**Files:**
- Modify: scripts/build-site.test.mjs
- Modify: scripts/build-site.mjs

**Interfaces:**
- Consumes: ordered boards, active board, and route base from Task 2.
- Produces: renderAgentNav(), renderHistoryRows(), renderRedirect(), unified shell, and responsive CSS.

- [ ] **Step 1: Write a failing shell test**

Add this complete test:

~~~js
test("agent pages render vertical tabs, today state, history, and nested links", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "agent-shell-"));
  const runsDir = path.join(tempDir, "runs");
  const workbuddyRunsDir = path.join(tempDir, "runs-workbuddy");
  const agentsRunsDir = path.join(tempDir, "runs-agents");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(agentsRunsDir, "2026-07-04", "alice--review.json"), {
    agentId: "alice",
    agentName: "Alice Agent",
    agentRole: "Research",
    taskId: "daily-review",
    taskName: "Daily Review",
    status: "success",
    summary: "Historical Alice result."
  });

  await buildSite({
    runsDir,
    workbuddyRunsDir,
    agentsRunsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  const aliceHome = await fs.readFile(path.join(outDir, "agents", "alice", "index.html"), "utf8");
  assert.match(aliceHome, /class="agent-tabs"/);
  assert.match(aliceHome, /href="\.\.\/\.\.\/index\.html"/);
  assert.match(aliceHome, /href="\.\.\/\.\.\/workbuddy\.html"/);
  assert.match(aliceHome, /aria-current="page"[^>]*>[\s\S]*?<strong>Alice Agent<\/strong>/);
  assert.match(aliceHome, /Today/);
  assert.match(aliceHome, /History/);
  assert.match(aliceHome, /No Alice Agent automation results/);
  assert.match(aliceHome, /2026-07-04/);

  const aliceDay = await fs.readFile(
    path.join(outDir, "agents", "alice", "days", "2026-07-04.html"),
    "utf8"
  );
  assert.match(aliceDay, /href="\.\.\/\.\.\/\.\.\/index\.html"/);
  assert.match(aliceDay, /href="\.\.\/\.\.\/\.\.\/workbuddy\.html"/);

  await assertFileContains(path.join(outDir, "history.html"), "Codex History");
  await assertFileContains(path.join(outDir, "workbuddy-history.html"), "WorkBuddy History");
  await assertFileContains(path.join(outDir, "agents.html"), "agents/alice/index.html");
  await assertFileContains(path.join(outDir, "agent-history.html"), "agents/alice/index.html");
});
~~~

- [ ] **Step 2: Run it and verify RED**

    node --test --test-name-pattern="vertical tabs" scripts/build-site.test.mjs

Expected: FAIL because navigation is horizontal, home pages omit full history, and redirects do not exist.

- [ ] **Step 3: Integrate history into every home**

Extract renderHistoryRows(groupedByDay, board, base) from renderHistory(). Use it in renderHistory() and in a History section directly below the Today section. Remove the old Latest recorded day block. History links use:

~~~js
base + board.dayDir + "/" + date + ".html"
~~~

- [ ] **Step 4: Render the vertical shell**

Add:

~~~js
function renderAgentNav(boards, activeBoard, base) {
  return '<nav class="agent-tabs" aria-label="Agents">' +
    boards.map((entry) =>
      '<a ' + (entry.key === activeBoard.key ? 'aria-current="page"' : '') +
      ' href="' + base + entry.indexFile + '">' +
      '<strong>' + escapeHtml(entry.agentName) + '</strong>' +
      '<span>' + escapeHtml(entry.agentRole) + '</span></a>'
    ).join("") +
    "</nav>";
}
~~~

Change layout() to render a compact header, then an app-shell containing agent-sidebar and main. The sidebar calls renderAgentNav(boards, board, base). Remove the horizontal Today/History/WorkBuddy/Agents navigation.

- [ ] **Step 5: Add deterministic redirects**

~~~js
function renderRedirect(target) {
  const safeTarget = escapeHtml(target);
  return '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<meta http-equiv="refresh" content="0; url=' + safeTarget + '">' +
    '<link rel="canonical" href="' + safeTarget + '">' +
    '<title>Open agent · Daily Task Board</title></head>' +
    '<body><a href="' + safeTarget + '">Open agent</a></body></html>';
}
~~~

After rendering, write agents.html and agent-history.html to the first discovered Agent index, or index.html when none exists.

- [ ] **Step 6: Add responsive CSS**

Keep the existing card, status, and history-row rules, and replace the old header navigation and page-width rules with:

~~~css
.app-shell {
  display: grid;
  grid-template-columns: minmax(190px, 230px) minmax(0, 1fr);
  margin: 0 auto;
  max-width: 1440px;
  min-height: calc(100vh - 129px);
  width: 100%;
}

.agent-sidebar {
  align-self: start;
  border-right: 1px solid var(--line);
  min-height: calc(100vh - 64px);
  padding: 28px 16px;
  position: sticky;
  top: 64px;
}

.agent-tabs {
  display: grid;
  gap: 6px;
}

.agent-tabs a {
  border: 1px solid transparent;
  border-radius: 6px;
  color: var(--muted);
  display: grid;
  gap: 3px;
  min-width: 0;
  padding: 10px 12px;
  text-decoration: none;
}

.agent-tabs a[aria-current="page"] {
  background: #e5eeee;
  border-color: #c6d8d5;
  color: var(--accent-strong);
}

.agent-tabs strong,
.agent-tabs span {
  overflow-wrap: anywhere;
}

.agent-tabs span {
  font-size: 0.78rem;
  line-height: 1.35;
}

main {
  min-width: 0;
  padding: 36px clamp(20px, 4vw, 56px) 56px;
}

h1 {
  font-size: 2.5rem;
  line-height: 1.08;
  margin: 0;
}

@media (max-width: 760px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .agent-sidebar {
    border-bottom: 1px solid var(--line);
    border-right: 0;
    min-height: 0;
    padding: 18px 20px;
    position: static;
  }

  .agent-tabs {
    grid-template-columns: 1fr;
  }

  main {
    padding: 28px 20px 44px;
  }

  h1 {
    font-size: 2rem;
  }
}
~~~

- [ ] **Step 7: Verify GREEN and commit**

    node --test --test-name-pattern="vertical tabs" scripts/build-site.test.mjs
    npm test
    npm run build
    git add scripts/build-site.mjs scripts/build-site.test.mjs public
    git commit -m "feat: add vertical per-agent dashboard tabs"

---

### Task 4: Publish The Onboarding Guide And Verify The Site

**Files:**
- Create: AGENT_ONBOARDING.md
- Modify: AGENT_BOARD_CONTRACT.md
- Modify: README.md
- Modify: AGENTS.md
- Regenerate: public/

**Interfaces:**
- Consumes: the final result schema and generated routes.
- Produces: one copy-ready connection guide and repository docs that match the generator.

- [ ] **Step 1: Create AGENT_ONBOARDING.md**

Include a complete JSON example, required IDs and fields, first-run setup, build and commit commands, conflict recovery, and this copy-ready automation prompt:

~~~text
After completing a meaningful automated task, read AGENT_ONBOARDING.md and AGENT_BOARD_CONTRACT.md. Use the Asia/Shanghai date and write one valid JSON result to runs-agents/YYYY-MM-DD/<agent-id>--<task-id>.json. Keep agentId stable and include agentName, taskId, taskName, status, and summary. Pull main before writing. Run npm run build, commit the source JSON with generated public/ files, rebase on origin/main before pushing, rebuild after any rebase that changes repository content, and then push. Never edit public/ manually.
~~~

- [ ] **Step 2: Align existing guidance**

Revise AGENT_BOARD_CONTRACT.md to describe independent auto-discovered tabs and remove the “not important enough” wording. Update README.md with the route mapping Codex -> index.html, WorkBuddy -> workbuddy.html, other Agent -> agents/<agent-id>/index.html. Link AGENT_ONBOARDING.md first. Update AGENTS.md so non-built-in assistants read both onboarding and contract files.

- [ ] **Step 3: Verify stale claims are gone**

    rg -n "shared Agents tab|not important enough|one shared task board" README.md AGENT_BOARD_CONTRACT.md AGENT_ONBOARDING.md AGENTS.md

Expected: no matches.

- [ ] **Step 4: Run fresh automated verification**

    npm test
    npm run build
    git diff --check

Expected: all tests pass, build exits 0, and diff check has no output.

- [ ] **Step 5: Inspect desktop and mobile pages**

Open public/index.html and public/workbuddy.html around 1440x900 and 390x844. Confirm vertical tabs, active state, Today plus History, readable cards, no overlap, and mobile stacking. Open one day page and task page to verify nested navigation.

- [ ] **Step 6: Commit documentation and generated output**

    git add AGENT_ONBOARDING.md AGENT_BOARD_CONTRACT.md README.md AGENTS.md public
    git commit -m "docs: add multi-agent board onboarding guide"

- [ ] **Step 7: Final repository check**

    git status --short --branch
    git log --oneline -6

Expected: a clean worktree with implementation commits ahead of origin/main, ready to push together.
