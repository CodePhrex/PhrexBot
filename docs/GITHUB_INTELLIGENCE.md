# GitHub intelligence

The adapter discovers token-accessible repositories belonging to the configured owner, including organization memberships. Inventory is bounded to 10 pages by default (100 records per page across all owners), with explicit truncation. Activity returns the first page of up to 20 API records for commits, branches, issues, pull requests, releases and workflow runs. Issues exclude pull requests. No writes, redirects or arbitrary endpoints. API failures are not empty results.

This adapter is not yet exposed to Slack. Before enabling commands, enforce individual repository entitlement or restrict expanded intelligence to an explicitly authorized administrator. A service token is not proof of a Slack user's GitHub access. Additional repositories require token authorization. Do not log raw payloads or credentials. Project roadmap and cross-repository activity aggregation remain follow-up work.
