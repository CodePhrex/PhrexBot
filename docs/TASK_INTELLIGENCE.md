# Task intelligence

Administrator-controlled local JSON snapshot: `as_of` timezone-aware timestamp and `tasks` array. Each task has `name`, `status` (active/paused/unknown), optional `project`, `schedule`, `last_run` timezone-aware timestamp and `last_outcome` (success/failure/running/unknown). A known outcome requires an execution timestamp. Snapshots older than 24 hours are stale. Counts cover at most 100 returned tasks and are explicitly marked truncated when applicable. Active means configured active, not currently running. A failure count refers to recorded last outcomes, not a live alert feed.

No direct ChatGPT automation API or snapshot producer is implemented. Do not fabricate execution outcomes. The existing slash command remains unchanged; integration with the new adapter and administrator-only access are pending. Store snapshots outside the repository and restrict local file permissions. No secrets or raw task prompts.
