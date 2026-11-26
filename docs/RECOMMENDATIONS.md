# Decision support

Deterministic recommendations consume caller-validated project and workflow evidence. No action execution, model-generated facts, or deployment inference. Missing or stale evidence takes precedence. Future integration must authenticate requester, bind actual run IDs and timestamps, validate evidence freshness, render safe follow-up actions, and test live conversation continuity. Deferred under D06, D11 and D20 in TECHNICAL_DEBT.md. The current module does not independently fetch evidence or perform recommendations in Slack.
