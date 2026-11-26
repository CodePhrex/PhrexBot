# SVC-08 — Service migration and acceptance

Status: foundations only; NOT deployment-ready. Keep the existing scheduled task operational. No gate is certified by merging this document.

## Integration backlog (required before migration)

- INT-01: verify and pin WinSW release, validate XML schema and executable integrity; select compatible protected installation layout.
- INT-02: reconcile service_config credential names with bot configuration; implement explicit service data paths across launcher, locks, logging, knowledge and task stores. Test with isolated fixtures.
- INT-03: implement and test service-compatible runtime entry point and graceful shutdown; eliminate scheduler-specific exit mapping where inappropriate.
- INT-04: validate dedicated service identity, effective ACLs, protected configuration and secure database migration. Restricted plaintext configuration is not an encrypted vault.
- INT-05: implement reviewed installation/removal and rollback utilities with explicit administrator authorization; verify exclusive activation and preserve data.
- INT-06: integrate optional Ollama readiness and independent health collection; validate recovery behavior, alert deduplication and delivery.
- INT-07: run full regression and Windows service fixture tests; document exact revision, results and remaining limitations.

## Migration gates

Require evidence for each gate: exact revision and test reference, verified wrapper integrity, service identity/ACL validation, secure backup, service-compatible paths, graceful stop and recovery fixture, exclusive activation, explicit administrator approval. Stop and disable existing task only during approved cutover; verify owned processes exit before starting service. Never run both simultaneously.

## Live acceptance

Verify SCM state and application heartbeat, Slack response, GitHub access, database integrity, optional inference, no visible terminal, operation before sign-in and after sign-out, bounded recovery, graceful stop and rollback. Record timestamps and evidence without credentials. Do not certify pre-login operation from an interactive session test.

## Rollback

Stop and disable the service, verify owned processes exit, preserve service data and logs, restore compatible backed-up data if necessary, re-enable and start the prior scheduled task with approval, verify Slack response. Never delete data by default.

## Outstanding debt

All SVC-01 through SVC-07 documented limitations remain open until tested and deployed. Track D01-D03/D11/D18/D19 in TECHNICAL_DEBT.md. SVC-08 is an acceptance specification, not a completed migration. No installation, account provisioning or host mutation is performed by this document.
