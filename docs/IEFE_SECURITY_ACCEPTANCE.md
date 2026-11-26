# IEFE-11 security acceptance

Run from repository root: `python -m unittest discover -s tests`.

| Scope | Regression module |
|---|---|
| Owner isolation | test_execution_isolation |
| Bounded admission | test_inference_concurrency |
| Atomic retry and terminal transitions | test_execution_races |
| Cooperative stream deadline | test_stream_deadline |
| Retry privacy | test_retry_privacy |
| Final delivery failure | test_delivery_recovery |

## Release gates

- Record exact revision, clean working tree, test count, exit status and duration.
- Verify Windows and Linux CI independently; missing results are not passes.
- Restart only the authorized Phrex runtime; verify fresh startup and scheduled task state.
- Verify private Slack diagnostics and a natural request with terminal history.
- Use synthetic inputs for failure, cancellation and concurrency tests. Do not expose credentials or other members' private records.
- Record outstanding live multi-user isolation, sustained load, blocked-I/O deadlines, cancellation/delivery races and retry retention limitations in TECHNICAL_DEBT.md.

Passing unit tests does not establish comprehensive security or production acceptance. Do not close deferred items without evidence.
