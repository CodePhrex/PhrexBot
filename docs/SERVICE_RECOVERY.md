# SVC-06 — Shutdown and recovery

The pure service_lifecycle policy distinguishes requested stop, clean exit, duplicate refusal and unexpected failure. Proposed retry delays are 60, 120 and 300 seconds; after three attempts report exhaustion. The caller must maintain the failure count; no persistent counter or restart execution is implemented. Use one recovery owner (SCM/wrapper or supervisor), not competing loops. Define reset criteria and validate actual wrapper semantics before activation.

Shutdown contract: stop accepting new work, disconnect Slack, cancel or bound outstanding requests, close database connections, flush logs, and verify the exact owned child process tree exits. Never terminate unrelated Python processes. A timeout is not evidence of graceful shutdown; forced termination is a last resort and requires database integrity verification. Existing launcher uses blocking subprocess.run and scheduler-specific exit mapping; service integration must address both before deployment. Validate with controlled test fixtures, not the live production process.

Pending: actual shutdown hooks, process ownership, persistent failure accounting, SCM recovery configuration, database integrity checks, runtime integration and live acceptance. Track D01/D02/D19. Four policy tests added; execution not independently verified. No host changes.
