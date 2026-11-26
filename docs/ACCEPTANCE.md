# Production acceptance checklist

- [ ] CI passes on merged main.
- [ ] Slack app installed from manifest; Socket Mode and interactivity enabled.
- [ ] App-level and bot tokens stored locally, not committed.
- [ ] GitHub token restricted to selected repositories and read permissions.
- [ ] Host starts and maintains Socket Mode connection.
- [ ] Authorized user runs `/phrex help`, `status`, `builds`, `progress`, `digest`, `alerts`, `approvals`, `security`, and `tasks`.
- [ ] Non-allowlisted test user receives denial.
- [ ] Responses are ephemeral; repository buttons open expected GitHub URLs.
- [ ] Missing GitHub permissions produce unavailable results; absent task source is explicitly unavailable.
- [ ] Restart host and confirm reconnection.

Do not mark production accepted until live checks pass. See DEPLOYMENT.md. Task reporting requires an external snapshot producer.
