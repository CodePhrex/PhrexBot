"""Advisory heuristics, not service-level objectives or root-cause diagnosis."""
MIN_SAMPLES=10
EXECUTION_P95_SECONDS=30
QUEUE_P95_SECONDS=5

def recommendations(metrics, admissions):
    result=[]
    n=metrics["total"]
    if n<MIN_SAMPLES:
        result.append(f"Limited sample: {n}/{MIN_SAMPLES} terminal executions. Collect more observations before judging typical performance.")
    else:
        execution=metrics["execution_seconds"]
        queue=metrics["queue_seconds"]
        if execution and execution["p95"]>=EXECUTION_P95_SECONDS:
            result.append("Execution p95 is at least 30s. Profile model loading, inference and response delivery separately before tuning.")
        if queue and queue["p95"]>=QUEUE_P95_SECONDS:
            result.append("Queue p95 is at least 5s. Review workload timing and worker occupancy before increasing concurrency.")
    failed=metrics["outcomes"]["failed"]
    if failed:
        result.append(f"{failed} recorded failures. Review diagnostic failure codes; causes require investigation.")
    rejected=admissions["queue_full"]
    if rejected:
        result.append(f"{rejected} queue-full observations in the process-local last-hour window. Review admission pressure; this is not total historical rejection count.")
    if not result:
        result.append("No configured advisory threshold triggered in the observed sample. This does not establish system health.")
    return result
