# Workspace reconciliation

Compare authenticated PIX-07 snapshots by stable channel ID. Newly observed does not prove creation; missing does not prove deletion. Partial snapshots never generate missing-channel findings. Retain last observed metadata. Intended cadence: 15-minute reconciliation and daily audit. Event subscriptions, scheduling, durable change history, stale/out-of-order snapshot rejection, notification deduplication, private channel authorization and live tests remain deferred under D17. No scheduler or event handler activated by this change.
