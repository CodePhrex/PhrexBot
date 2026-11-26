# PhrexBot — CodePhrex Intelligence

**Intelligence on Command.**

Read-only Slack operations assistant using Slack Bolt Socket Mode and GitHub REST API. Initial MVP supports help, project status and build summaries. Other commands are explicitly unavailable until their adapters are implemented.

## Local setup
Python 3.11+. Install `pip install -r requirements.txt`. Create a Slack app using `slack-manifest.yml`, enable Socket Mode, generate an app-level token with connections:write, install the app and obtain its bot token. Configure environment variables from `.env.example` in your shell or secret manager (the app does not automatically load .env). Use a fine-grained GitHub token with read-only metadata, pull requests and actions access to selected repositories. Run `python bot.py`. Never commit tokens.

Run `python -m unittest discover -s tests` for tests. Docker: build with `docker build -t phrexbot .` and run with `docker run --env-file .env phrexbot`.

No direct ChatGPT automation API is assumed. Production deployment and Slack authorization remain required.
