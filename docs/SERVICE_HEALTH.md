# SVC-07 — Service health assessment

The assessment module classifies supplied timestamped observations, not live telemetry. Core checks: SCM service state, owned runtime, Slack connectivity, database access. Optional dependency checks: GitHub and Ollama. Default evidence freshness is five minutes. Missing, stale or future observations are unknown. Optional disabled states are allowed; core disabled is unverified. Healthy means all required supplied observations are fresh and positive and optional dependencies are positive or disabled, not independently authenticated.

Production monitoring must independently collect actual observations, distinguish SCM state from application heartbeat, validate database access without exposing content, and verify Slack connectivity and inference separately. Do not treat model listing as inference success. Alerts require deduplication, recovery notices and an independent delivery path when the bot is down. No secret values or raw exception bodies in reports.

Pending: live collectors, independent scheduling, durable alert state, delivery, integration with existing runtime health, Windows tests and acceptance. Track D01/D02/D19. Five unit tests added; execution not independently verified. No host changes.
