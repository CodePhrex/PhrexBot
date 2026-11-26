# SVC-05 — Optional local inference

Phrex service startup must not depend on Ollama startup. Deterministic commands should remain available during inference outages. ollama_readiness.py probes only the fixed loopback model-list endpoint with connect/read timeouts and no redirects. Model listing is not proof of successful inference; inference_ready remains false until separately validated. No downloads, process launches or configuration changes occur.

Before production migration, verify Ollama availability before sign-in under the selected service identity, model storage access, loopback binding and resource capacity. Do not expose the inference endpoint externally. User-session Ollama availability is not evidence of pre-login operation. If unavailable, report degraded inference and retain deterministic commands. Integrate the probe with service diagnostics and test real inference and recovery separately.

Pending: independent Ollama provisioning, runtime wiring, bounded retry scheduling, actual inference validation, Windows service acceptance. Track under D01/D02/D11/D19. Mocked tests added; live behavior not certified.
