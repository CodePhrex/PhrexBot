# Phrex Windows Service — SVC-01

## Target
Service ID PhrexIntelligence; display name CodePhrex Intelligence Service. WinSW wrapper, Python runtime, automatic delayed startup, dedicated least-privilege identity. No installation in this milestone.

## Boundaries
Service binaries and application code must be administrator-controlled, not writable by ordinary users. Use a separately provisioned service-compatible Python environment; do not assume the current user venv works under a different identity. Explicit machine-level data directory with restricted ACLs for configuration, SQLite databases, logs and locks. Do not copy secrets into XML, command lines or logs. Provision credentials securely for the service identity. Never default to LocalSystem. Verify wrapper release provenance and integrity before use.

## Dependencies
Slack and GitHub require network availability; use bounded retries. Ollama is optional and must be separately available before sign-in to support local inference; deterministic commands must remain usable when inference is unavailable. No assumption that user-session Ollama is reachable at boot. Use one shared instance-lock location across migration modes, or enforce mutually exclusive activation before startup. Validate graceful termination of child processes and SQLite integrity.

## Migration
Keep existing scheduled task CodePhrex - Phrex AI operational during development. Before service activation, obtain explicit administrator authorization, verify tests and paths, back up databases securely, stop and disable the scheduled task, verify its child processes have exited, provision service identity and restricted data directory, install and validate service. Never run both instances concurrently. Rollback: stop and disable service, verify exit, restore compatible data if necessary, re-enable and start scheduled task. Preserve credentials and backups.

## Acceptance
Verify service identity and ACLs, no visible terminal, startup before sign-in, operation after sign-out, Slack command response, GitHub access, optional Ollama availability, bounded restart after controlled failure, graceful stop, no duplicate processes, diagnostic logs and rollback. No gate is certified by this design.

## Roadmap
SVC-01 architecture; SVC-02 wrapper configuration; SVC-03 installation/removal utilities; SVC-04 identity and credentials; SVC-05 Ollama dependencies; SVC-06 shutdown and recovery; SVC-07 health monitoring; SVC-08 migration and acceptance. Track under D01-D03 and D18/D19 in TECHNICAL_DEBT.md.
