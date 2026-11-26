# Persistent Windows runtime

Use Windows Task Scheduler under the current interactive user, without elevation. Do not change execution policy. Review and authorize the launcher before registering it. Do not run a second instance alongside an existing bot.

## Acceptance criteria
- Start at user sign-in; no stored account password.
- Task instance policy: IgnoreNew. This prevents duplicate scheduled instances, not manually started copies.
- Restart on failure with a one-minute delay and a bounded retry count.
- No execution time limit; explicitly stop the task for maintenance.
- Store diagnostic logs outside the repository under LocalAppData; never log environment variables, tokens, or raw request bodies.
- Verify Slack response, repository inventory freshness and task status after startup.
- Verify recovery after a controlled failure and after sign-out/sign-in.
- Runtime failure alerts require an independent monitor; an offline bot cannot reliably notify Slack itself.

## Rollback
Disable the scheduled task, stop its running instance, and return to the documented foreground launcher. Preserve the project database and .env. Do not delete credentials or change system-wide policy.

## Deployment status
This document is a design and acceptance checklist, not evidence that a scheduled task has been registered. Windows launcher implementation, log rotation, independent monitoring and host acceptance remain separate deliverables.
