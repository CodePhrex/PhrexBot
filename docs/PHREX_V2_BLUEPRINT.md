# Phrex Intelligence Platform v2.0

Approved 2026-11-25. CodePhrex Intelligence — Intelligence on Command.

## Identity
User-facing name Phrex; repository CodePhrex/PhrexBot; slash command /phrex; preferred channels #phrex and #phrex-help (rename pending). Preserve existing commands. Palette: #030711, #081525, #006CFF, #00D9FF, #8B35FF, #E8F2FF. Orbitron headings, Inter body, JetBrains Mono technical graphics; Slack native typography for interactive messages. Use generated graphics and attachment accents where supported, accessible text alternatives and validated URLs.

## Architecture
Slack commands, mentions and DMs; authorized routing and optional local Ollama/cloud inference; GitHub read-only discovery; Windows telemetry; persistent SQLite project knowledge and audit records; graphical reports and validated app links. Distinguish verified facts, plans, estimates and unavailable data. No fabricated completion metrics. Preserve existing runtime until tested replacement.

## Roadmap
1. PX-01 Identity and blueprint.
2. PX-02 Graphics and typography engine.
3. PX-03 Persistent project knowledge: purpose, blueprint, repository, stack, milestones, issues, deployment, dependencies and branding.
4. PX-04 Organization-wide GitHub intelligence: repos, project, commits, PRs, builds, issues, roadmap, releases, security, activity.
5. PX-05 Windows telemetry: CPU, RAM, disks, network, processes, services, software, uptime, diagnostics. Administrator-only; no credentials or private file content.
6. PX-06 Validated URL and application link engine.
7. PX-07 Natural-language inference with controlled read-only tools.
8. PX-08 Slack mentions and DMs, scoped event subscriptions.
9. PX-09 Scheduled task intelligence, supported integration only; otherwise labeled local snapshots.
10. PX-10 Executive dashboard and graphical reports.
11. PX-11 Security, permissions, audit and credential storage.
12. PX-12 Regression tests, production deployment, startup persistence and live acceptance.

## Security gates
Enforce authorization from the first feature that accesses new data; do not defer security until PX-11. Host data restricted to explicitly authorized administrators. Private repository access must respect user entitlement; no automatic expansion to workspace-wide private data. Read-only defaults, no arbitrary shell execution from Slack, no secret disclosure, no unapproved destructive operations. Treat repository and retrieved text as untrusted. AI providers optional and explicitly configured; minimize data sent externally. Validate links against trusted destinations. Audit without secrets. Additional Slack scopes, provider credentials and GitHub permissions require administrator approval.

## Acceptance
Each sprint requires tests and review. Actual Slack display name, channel renames and new scopes require Slack configuration. Live task access depends on a supported integration. No claims of live deployment until runtime and command acceptance are verified.
