# Deployment

1. Ensure repository visibility is private.
2. Visit https://api.slack.com/apps and create an app from the repository manifest. Enable Socket Mode and Interactivity for URL button callbacks. Generate an app-level token with connections:write. Install to your workspace and obtain the bot token.
3. Create a fine-grained GitHub token limited to selected repositories: Metadata, Contents, Pull requests, Actions and Dependabot alerts read access as supported. Never paste tokens into chat or commit them.
4. Copy .env.example to .env locally. Set SLACK_TEAM_ID and SLACK_ALLOWED_USERS to actual Slack IDs, and populate tokens. Verify the configured repository list. Optional task snapshots require a read-only mount and PHREX_TASK_SNAPSHOT.
5. With Docker running, execute `docker compose up -d --build` then `docker compose logs --tail=50 phrexbot`. Stop with `docker compose down`.
6. Test `/phrex help`, `/phrex status droidlab`, `/phrex builds`, and unauthorized access using a separate non-allowlisted test account. Confirm responses are ephemeral. Test repository buttons and data unavailable behavior.

No public port is needed. Keep the host online. Rotate tokens if exposed. Audit logs record accepted/denied commands without raw command content or credentials. Live validation is required before production acceptance.
