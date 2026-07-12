import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import {
  CODEX_BOARD,
  WORKBUDDY_BOARD,
  buildSite,
  collectRuns,
  createDiscoveredAgentBoards,
  dateInTimeZone,
  normalizeRun,
  RESERVED_AGENT_IDS
} from "./build-site.mjs";

test("dateInTimeZone returns the Asia/Shanghai calendar date", () => {
  const date = new Date("2026-07-04T18:00:00.000Z");
  assert.equal(dateInTimeZone(date, "Asia/Shanghai"), "2026-07-05");
});

test("normalizeRun validates and normalizes a result file", () => {
  const filePath = path.join(os.tmpdir(), "runs", "2026-07-05", "daily-review.json");
  const run = normalizeRun(
    {
      taskId: "daily-review",
      taskName: "Daily Review",
      status: "needs_attention",
      startedAt: "2026-07-05T08:00:00+08:00",
      finishedAt: "2026-07-05T08:01:30+08:00",
      summary: "Review needs follow-up.",
      details: "One item needs a decision.",
      labels: ["review"],
      nextSteps: ["Decide the owner."],
      artifacts: [{ label: "Notes", path: "notes.md" }]
    },
    filePath,
    path.join(os.tmpdir())
  );

  assert.equal(run.date, "2026-07-05");
  assert.equal(run.taskId, "daily-review");
  assert.equal(run.duration, "1m 30s");
  assert.deepEqual(run.labels, ["review"]);
  assert.equal(run.sourceFile, "runs/2026-07-05/daily-review.json");
});

test("normalizeRun supports required personal agent attribution", () => {
  const filePath = path.join(os.tmpdir(), "runs-agents", "2026-07-05", "alice--daily-review.json");
  const run = normalizeRun(
    {
      agentId: "alice-agent",
      agentName: "Alice Agent",
      agentRole: "Personal research assistant",
      taskId: "daily-review",
      taskName: "Daily Review",
      status: "success",
      summary: "Review completed."
    },
    filePath,
    path.join(os.tmpdir()),
    { requireAgent: true }
  );

  assert.equal(run.agentId, "alice-agent");
  assert.equal(run.agentName, "Alice Agent");
  assert.equal(run.agentRole, "Personal research assistant");
});

test("normalizeRun rejects shared agent records without agentId", () => {
  const filePath = path.join(os.tmpdir(), "runs-agents", "2026-07-05", "daily-review.json");
  assert.throws(
    () =>
      normalizeRun(
        {
          taskId: "daily-review",
          taskName: "Daily Review",
          status: "success",
          summary: "Review completed."
        },
        filePath,
        path.join(os.tmpdir()),
        { requireAgent: true }
      ),
    /agentId/
  );
});

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

test("normalizeRun requires external agentId values to already be safe slugs", () => {
  const filePath = path.join(os.tmpdir(), "runs-agents", "2026-07-05", "agent--review.json");
  const baseRun = {
    agentName: "External Agent",
    taskId: "daily-review",
    taskName: "Daily Review",
    status: "success",
    summary: "Review completed."
  };

  for (const agentId of ["Uppercase-Agent", " padded-agent ", "agent/with/slashes"]) {
    assert.throws(
      () => normalizeRun({ ...baseRun, agentId }, filePath, path.join(os.tmpdir()), { requireAgent: true }),
      (error) => {
        assert.match(error.message, new RegExp(filePath.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
        assert.match(error.message, /agentId/);
        assert.match(error.message, /2-81 character slug/);
        assert.match(error.message, /lowercase letters, numbers, dots, underscores, or hyphens/);
        return true;
      },
      agentId
    );
  }

  for (const agentId of RESERVED_AGENT_IDS) {
    assert.throws(
      () => normalizeRun({ ...baseRun, agentId }, filePath, path.join(os.tmpdir()), { requireAgent: true }),
      new RegExp(`reserved agentId "${agentId}"`)
    );
  }
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

test("collectRuns reads nested result JSON files in descending order", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "codex-runs-"));
  const runsDir = path.join(tempDir, "runs");

  await writeJson(path.join(runsDir, "2026-07-04", "older.json"), {
    taskId: "older-task",
    taskName: "Older Task",
    status: "success",
    summary: "Older result"
  });

  await writeJson(path.join(runsDir, "2026-07-05", "newer.json"), {
    taskId: "newer-task",
    taskName: "Newer Task",
    status: "success",
    summary: "Newer result"
  });

  const runs = await collectRuns(runsDir, tempDir);
  assert.equal(runs.length, 2);
  assert.equal(runs[0].taskId, "newer-task");
  assert.equal(runs[1].taskId, "older-task");
});

test("buildSite uses a total run order for board metadata, feeds, tabs, and legacy redirects", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "agent-order-"));
  const runsDir = path.join(tempDir, "runs");
  const agentsRunsDir = path.join(tempDir, "runs-agents");
  const outDir = path.join(tempDir, "public");
  const date = "2026-07-05";
  const finishedAt = "2026-07-05T08:00:00+08:00";
  const baseRun = {
    taskId: "same-task",
    taskName: "Same Task",
    status: "success",
    summary: "Tied result.",
    finishedAt
  };

  await writeJson(path.join(agentsRunsDir, date, "zeta--same-task.json"), {
    ...baseRun,
    agentId: "zeta",
    agentName: "Shared Name",
    agentRole: "Zeta role"
  });
  await writeJson(path.join(agentsRunsDir, date, "alpha--same-task.json"), {
    ...baseRun,
    agentId: "alpha",
    agentName: "Shared Name",
    agentRole: "Alpha role"
  });
  await writeJson(path.join(agentsRunsDir, date, "metadata--z.json"), {
    ...baseRun,
    agentId: "metadata",
    agentName: "Metadata Loser",
    agentRole: "Loser role"
  });
  await writeJson(path.join(agentsRunsDir, date, "metadata--a.json"), {
    ...baseRun,
    agentId: "metadata",
    agentName: "Metadata Winner",
    agentRole: "Winner role"
  });

  const tiedRuns = [
    { ...baseRun, agentId: "zeta", agentName: "Shared Name", agentRole: "Zeta role", date, sourceFile: `runs-agents/${date}/zeta--same-task.json` },
    { ...baseRun, agentId: "alpha", agentName: "Shared Name", agentRole: "Alpha role", date, sourceFile: `runs-agents/${date}/alpha--same-task.json` },
    { ...baseRun, agentId: "metadata", agentName: "Metadata Loser", agentRole: "Loser role", date, sourceFile: `runs-agents/${date}/metadata--z.json` },
    { ...baseRun, agentId: "metadata", agentName: "Metadata Winner", agentRole: "Winner role", date, sourceFile: `runs-agents/${date}/metadata--a.json` }
  ];
  const boards = createDiscoveredAgentBoards(tiedRuns);
  assert.deepEqual(boards.map(({ board }) => board.key), ["metadata", "alpha", "zeta"]);
  assert.equal(boards[0].board.agentName, "Metadata Winner");
  assert.equal(boards[0].board.agentRole, "Winner role");

  await buildSite({
    runsDir,
    agentsRunsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  const feed = JSON.parse(await fs.readFile(path.join(outDir, "data", "agent-runs.json"), "utf8"));
  assert.deepEqual(feed.runs.map((run) => run.sourceFile), [
    `runs-agents/${date}/alpha--same-task.json`,
    `runs-agents/${date}/metadata--a.json`,
    `runs-agents/${date}/metadata--z.json`,
    `runs-agents/${date}/zeta--same-task.json`
  ]);

  const metadataHome = await fs.readFile(path.join(outDir, "agents", "metadata", "index.html"), "utf8");
  assert.match(metadataHome, /Metadata Winner/);
  assert.match(metadataHome, /Winner role/);
  assert.ok(metadataHome.indexOf('href="../../agents/alpha/index.html"') < metadataHome.indexOf('href="../../agents/zeta/index.html"'));
  await assertFileContains(path.join(outDir, "agents.html"), "url=agents/metadata/index.html");
  await assertFileContains(path.join(outDir, "agent-history.html"), "url=agents/metadata/index.html");
});

test("buildSite writes root, history, day, task, and data files", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "codex-site-"));
  const runsDir = path.join(tempDir, "runs");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(runsDir, "2026-07-05", "example-task.json"), {
    taskId: "example-task",
    taskName: "Example Task",
    status: "success",
    startedAt: "2026-07-05T08:00:00+08:00",
    finishedAt: "2026-07-05T08:02:00+08:00",
    summary: "Example completed.",
    details: "Everything finished normally."
  });

  const result = await buildSite({
    runsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  assert.equal(result.runCount, 1);
  await assertFileContains(path.join(outDir, "index.html"), "Example Task");
  await assertFileContains(path.join(outDir, "history.html"), "2026-07-05");
  await assertFileContains(path.join(outDir, "days", "2026-07-05.html"), "Example completed.");
  await assertFileContains(path.join(outDir, "tasks", "example-task.html"), "historical result");
  await assertFileContains(path.join(outDir, "data", "runs.json"), "example-task");
});

test("buildSite includes the WorkBuddy agent tab on all board pages", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "codex-nav-"));
  const runsDir = path.join(tempDir, "runs");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(runsDir, "2026-07-05", "example-task.json"), {
    taskId: "example-task",
    taskName: "Example Task",
    status: "success",
    summary: "Example completed."
  });

  await buildSite({
    runsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  await assertFileContains(path.join(outDir, "index.html"), "WorkBuddy");
  await assertFileContains(path.join(outDir, "index.html"), 'href="workbuddy.html"');
  await assertFileContains(path.join(outDir, "history.html"), 'href="workbuddy.html"');
  await assertFileContains(path.join(outDir, "days", "2026-07-05.html"), 'href="../workbuddy.html"');
  await assertFileContains(path.join(outDir, "tasks", "example-task.html"), 'href="../workbuddy.html"');
});

test("buildSite generates WorkBuddy board pages from runs-workbuddy", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "workbuddy-site-"));
  const runsDir = path.join(tempDir, "runs");
  const workbuddyRunsDir = path.join(tempDir, "runs-workbuddy");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(runsDir, "2026-07-05", "codex-task.json"), {
    taskId: "codex-task",
    taskName: "Codex Task",
    status: "success",
    summary: "Codex result."
  });

  await writeJson(path.join(workbuddyRunsDir, "2026-07-05", "wb-task.json"), {
    taskId: "wb-task",
    taskName: "WorkBuddy Task",
    status: "success",
    summary: "WorkBuddy result."
  });

  const result = await buildSite({
    runsDir,
    workbuddyRunsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  assert.equal(result.runCount, 1);
  assert.equal(result.workbuddyRunCount, 1);

  // WorkBuddy index page
  await assertFileContains(path.join(outDir, "workbuddy.html"), "WorkBuddy Task");
  await assertFileContains(path.join(outDir, "workbuddy.html"), 'aria-current="page"');
  // WorkBuddy history page
  await assertFileContains(path.join(outDir, "workbuddy-history.html"), "All recorded WorkBuddy days");
  // WorkBuddy day page
  await assertFileContains(path.join(outDir, "workbuddy-days", "2026-07-05.html"), "WorkBuddy result.");
  // WorkBuddy task page
  await assertFileContains(path.join(outDir, "workbuddy-tasks", "wb-task.html"), "historical result");
  // WorkBuddy data feed
  await assertFileContains(path.join(outDir, "data", "workbuddy-runs.json"), "wb-task");

  // Codex pages must NOT contain WorkBuddy run data
  const codexIndex = await fs.readFile(path.join(outDir, "index.html"), "utf8");
  assert.ok(!codexIndex.includes("WorkBuddy result."), "Codex index must not contain WorkBuddy run data");
  assert.ok(!codexIndex.includes("wb-task"), "Codex index must not link to WorkBuddy task pages");

  // WorkBuddy pages must NOT contain Codex run data
  const wbIndex = await fs.readFile(path.join(outDir, "workbuddy.html"), "utf8");
  assert.ok(!wbIndex.includes("Codex result."), "WorkBuddy index must not contain Codex run data");
  assert.ok(!wbIndex.includes("codex-task"), "WorkBuddy index must not link to Codex task pages");
});

test("buildSite handles empty WorkBuddy directory gracefully", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "workbuddy-empty-"));
  const runsDir = path.join(tempDir, "runs");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(runsDir, "2026-07-05", "codex-task.json"), {
    taskId: "codex-task",
    taskName: "Codex Task",
    status: "success",
    summary: "Codex result."
  });

  const result = await buildSite({
    runsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  assert.equal(result.workbuddyRunCount, 0);
  await assertFileContains(path.join(outDir, "workbuddy.html"), "No WorkBuddy automation results");
  await assertFileContains(path.join(outDir, "workbuddy-history.html"), "No WorkBuddy history");
});

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

test("buildSite preserves the combined personal agent feed alongside isolated pages", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "agents-site-"));
  const runsDir = path.join(tempDir, "runs");
  const agentsRunsDir = path.join(tempDir, "runs-agents");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(runsDir, "2026-07-05", "codex-task.json"), {
    taskId: "codex-task",
    taskName: "Codex Task",
    status: "success",
    summary: "Codex result."
  });

  await writeJson(path.join(agentsRunsDir, "2026-07-05", "alice--market-scan.json"), {
    agentId: "alice-agent",
    agentName: "Alice Agent",
    agentRole: "Market scanner",
    taskId: "market-scan",
    taskName: "Market Scan",
    status: "success",
    summary: "Agent result."
  });

  const result = await buildSite({
    runsDir,
    agentsRunsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  assert.equal(result.agentRunCount, 1);
  assert.equal(result.agentCount, 1);
  assert.equal(result.agentDayCount, 1);
  assert.equal(result.agentTaskCount, 1);
  await assertFileContains(path.join(outDir, "agents", "alice-agent", "index.html"), "Market Scan");
  await assertFileContains(path.join(outDir, "agents", "alice-agent", "days", "2026-07-05.html"), "Agent result.");
  await assertFileContains(path.join(outDir, "agents", "alice-agent", "tasks", "market-scan.html"), "Market scanner");
  await assertFileContains(path.join(outDir, "data", "agents", "alice-agent.json"), "alice-agent");
  await assertFileContains(path.join(outDir, "data", "agent-runs.json"), "alice-agent");

  const codexIndex = await fs.readFile(path.join(outDir, "index.html"), "utf8");
  assert.ok(!codexIndex.includes("Agent result."), "Codex index must not contain shared agent run data");
});

test("buildSite handles empty personal agent data gracefully", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "agents-empty-"));
  const runsDir = path.join(tempDir, "runs");
  const outDir = path.join(tempDir, "public");

  await writeJson(path.join(runsDir, "2026-07-05", "codex-task.json"), {
    taskId: "codex-task",
    taskName: "Codex Task",
    status: "success",
    summary: "Codex result."
  });

  const result = await buildSite({
    runsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  assert.equal(result.agentRunCount, 0);
  assert.equal(result.agentCount, 0);
  assert.equal(result.agentDayCount, 0);
  assert.equal(result.agentTaskCount, 0);
  await assertFileContains(path.join(outDir, "data", "agent-runs.json"), '"runs": []');
  await assertFileContains(path.join(outDir, "agents.html"), "url=index.html");
  await assertFileContains(path.join(outDir, "agent-history.html"), "url=index.html");
});

test("CODEX_BOARD and WORKBUDDY_BOARD have distinct directories and files", () => {
  assert.notEqual(CODEX_BOARD.dayDir, WORKBUDDY_BOARD.dayDir);
  assert.notEqual(CODEX_BOARD.taskDir, WORKBUDDY_BOARD.taskDir);
  assert.notEqual(CODEX_BOARD.indexFile, WORKBUDDY_BOARD.indexFile);
  assert.notEqual(CODEX_BOARD.historyFile, WORKBUDDY_BOARD.historyFile);
  assert.notEqual(CODEX_BOARD.dataFile, WORKBUDDY_BOARD.dataFile);
});

test("generated CSS wraps every unrestricted long card field", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "details-wrap-"));
  const runsDir = path.join(tempDir, "runs");
  const outDir = path.join(tempDir, "public");

  await buildSite({
    runsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  const styles = await fs.readFile(path.join(outDir, "assets", "styles.css"), "utf8");
  for (const selector of [".details", ".task-link", ".labels span", ".next-steps li", ".artifact-path", ".meta-line"]) {
    assert.match(styles, new RegExp(selector.replace(".", "\\.").replace(" ", "\\s+") + "\\s*\\{[^}]*overflow-wrap:\\s*anywhere;", "s"));
  }
  for (const selector of [".run-card", ".run-card-header > div", ".run-meta", ".labels", ".subsection"]) {
    assert.match(styles, new RegExp(selector.replace(".", "\\.").replace(" > ", "\\s*>\\s*").replace(" ", "\\s+") + "\\s*\\{[^}]*min-width:\\s*0;", "s"));
  }
});

test("generated CSS bounds the desktop agent sidebar and resets it on mobile", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "sidebar-scroll-"));
  const runsDir = path.join(tempDir, "runs");
  const outDir = path.join(tempDir, "public");

  await buildSite({
    runsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  const styles = await fs.readFile(path.join(outDir, "assets", "styles.css"), "utf8");
  assert.match(styles, /\.agent-sidebar\s*\{[^}]*max-height:\s*calc\(100vh - 64px\);[^}]*overflow-y:\s*auto;/s);
  assert.match(styles, /@media \(max-width: 760px\)\s*\{[\s\S]*?\.agent-sidebar\s*\{[^}]*max-height:\s*none;[^}]*overflow-y:\s*visible;/);
});

test("buildSite renders long values in every unrestricted card field", async () => {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "long-card-fields-"));
  const runsDir = path.join(tempDir, "runs");
  const outDir = path.join(tempDir, "public");
  const longToken = "x".repeat(180);
  const longValues = {
    taskName: `Task-${longToken}`,
    summary: `Summary-${longToken}`,
    details: `Details-${longToken}`,
    sourceThread: `Source-${longToken}`,
    label: `Label-${longToken}`,
    nextStep: `Next-${longToken}`,
    artifactLabel: `Artifact-${longToken}`,
    artifactPath: `artifacts/${longToken}.json`
  };

  await writeJson(path.join(runsDir, "2026-07-05", "long-card.json"), {
    taskId: "long-card",
    taskName: longValues.taskName,
    status: "success",
    summary: longValues.summary,
    details: longValues.details,
    sourceThread: longValues.sourceThread,
    labels: [longValues.label],
    nextSteps: [longValues.nextStep],
    artifacts: [{ label: longValues.artifactLabel, path: longValues.artifactPath }]
  });

  await buildSite({
    runsDir,
    outDir,
    now: new Date("2026-07-05T02:00:00.000Z"),
    timeZone: "Asia/Shanghai"
  });

  const index = await fs.readFile(path.join(outDir, "index.html"), "utf8");
  for (const value of Object.values(longValues)) {
    assert.ok(index.includes(value));
  }
  assert.match(index, /class="subsection next-steps"/);
  assert.match(index, /class="artifact-path"/);
});

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

  const aliceTask = await fs.readFile(
    path.join(outDir, "agents", "alice", "tasks", "daily-review.html"),
    "utf8"
  );
  assert.match(aliceTask, /href="\.\.\/\.\.\/\.\.\/index\.html"/);
  assert.match(aliceTask, /href="\.\.\/\.\.\/\.\.\/workbuddy\.html"/);

  await assertFileContains(path.join(outDir, "history.html"), "Codex History");
  await assertFileContains(path.join(outDir, "workbuddy-history.html"), "WorkBuddy History");
  await assertFileContains(path.join(outDir, "agents.html"), "agents/alice/index.html");
  await assertFileContains(path.join(outDir, "agent-history.html"), "agents/alice/index.html");
});

async function writeJson(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function assertFileContains(filePath, expected) {
  const content = await fs.readFile(filePath, "utf8");
  assert.match(content, new RegExp(expected.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
}
