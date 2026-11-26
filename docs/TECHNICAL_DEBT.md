# Phrex technical debt and deferred acceptance register

All entries are open unless verified and explicitly closed with evidence. This register consolidates known limitations from prior development; it is not a fresh production audit. Review at every sprint and before PIX-14. Do not treat merged foundations as deployed capabilities.

| ID | Area | Outstanding work / acceptance |
|---|---|---|
| D01 | Runtime | Activate new launcher, verify single instance, register current-user startup task, test sign-in and bounded crash recovery; no elevation or execution-policy weakening. |
| D02 | Health | Schedule independent monitoring, verify Slack connectivity, deduplicate alerts, recovery notices and live delivery; process observation is not connectivity. |
| D03 | Logging | Validate rotation and failure coverage; durable audit and credential vault remain outstanding. |
| D04 | Identity | Confirm Slack app display name Phrex, official icon, channel renames and branding consistency. |
| D05 | Formatting | Verify actual Slack rendering; native fonts/colors restricted. Review 400-character row truncation and preserve material findings. |
| D06 | Links | General app registry, validated contextual URLs, interactive callback actions, authorization and live tests. Current incident links limited to six per project. |
| D07 | Graphics | Install licensed Orbitron/Inter/JetBrains Mono locally, configure font paths, replace simplified monogram with approved artwork, validate fallback and visual quality. |
| D08 | Delivery | Connect graphical reports/charts to authorized private Slack delivery; scope approval, accessible text, upload errors and live validation. |
| D09 | Charts | Bind verified live data; historical collection, line graphs, meaningful units and provenance. Current bar charts max 12 categories; diagrams max six nodes. |
| D10 | Memory | Explicit opt-in, Slack and inference integration, user-facing recall/delete controls, secret filtering, encryption/access controls, scheduled expiration, backup retention and secure-erasure limitations. Current plaintext SQLite, logical deletion, expiry on access; admin-only foundation, 30-day default, 20 stored turns, five recalled, 12000 characters. |
| D11 | AI | Integrate evidence into DM/mention routing; enable authorized Slack event scopes, verify actual delivery; correct model self-description and avoid claims of training. Validate host evidence schema and natural command routing. |
| D12 | Knowledge | Expand source-attributed project docs, resolve missing repository docs and alias matching, distinguish legacy Chirp, verified facts vs plans, avoid stale evidence. |
| D13 | Discovery | Verify recurring scans and notifications, stable aliases and rename reconciliation, SHA-based incremental document sync, blueprint ingestion, concurrency and durable retries. |
| D14 | GitHub | Integrate organization-wide discovery and activity into commands; verify token coverage, pagination and individual access controls; no workspace-wide private data expansion. |
| D15 | Host | Integrate admin-only PC commands, services/software/diagnostics and live telemetry validation; no arbitrary remote shell. |
| D16 | Tasks | Implement authorized snapshot producer and integrate validated task store; no live automation API assumed. Verify scheduled Slack delivery independently. |
| D17 | Workspace | Authorized Slack discovery, stable channel IDs, rename/archive events, reconciliation, docs knowledge, app/emoji metadata, Home/help, requester-level permissions. |
| D18 | Security | Durable rate limits/audit where needed, secret protection, cross-user isolation, untrusted content handling, scope approval and security acceptance. |
| D19 | Production | Run full CI and Windows regression suite, verify actual runtime revision, Slack responses and delivery, rollback, startup and recovery. |
| D20 | Reporting | Review neutral status semantics, no inferred approval/health/deployment; verify workflow links against real report format and disclose omitted data. |

## Closure policy
For each item record PR, test evidence, deployment revision and live acceptance where applicable. Add newly identified limitations here rather than losing them in chat. Prioritize privacy/security and runtime blockers before enabling affected features. Deferred work must not be silently advertised as available.

## IEFE deferred acceptance and remediation

- D01: Scheduled task stop can leave child inference processes; service integration, graceful stop, wrapper checksum and recovery acceptance remain open.
- D11/D18: Cooperative cancellation cannot interrupt blocked I/O; total streaming deadline, callback propagation, retry expiry without access, secret filtering, retry rollback and cancellation races require integration tests. Progress budget can exhaust before heartbeat; no native typing or partial text delivery.
- D19/D20: Terminal telemetry omits some admission/registration/submission failures and may be skipped on registry errors. Completion is not answer accuracy; durations include delivery. First-token and generation timing, actual time-weighted utilization, persistent rejection history, administrator aggregates and live model probes remain open. Queue observations are volatile, capped and owner-scoped. Upstream swallowed errors may be misclassified; legacy failure codes unknown. Diagnostic reports are plain text; live Slack and concurrency acceptance pending.
- D18: Execution metadata contains workspace/user identifiers. Hourly logical cleanup while running is not guaranteed physical erasure; existing write-time pruning, filesystem ACLs, backups, journals, offline retention, user deletion controls and service identity isolation need review. Do not claim encrypted storage or guaranteed erasure. No prompt or answer columns in execution history.
