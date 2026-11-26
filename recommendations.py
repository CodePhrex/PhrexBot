"""Read-only decision support for authenticated operational evidence."""

def recommend(*, project=None, workflow=None, evidence_available=False, stale=False):
    if not project:
        return {"classification":"clarification","question":"Which project should I investigate?","actions":[]}
    if not evidence_available or stale:
        return {"classification":"insufficient_evidence","question":"Would you like to refresh the repository evidence?","actions":["Verify repository access and evidence freshness."]}
    if workflow in ("failure","timed_out"):
        return {"classification":"observed_workflow_failure","question":"Would you like to inspect the failed workflow logs?","actions":["Review the failed run and its job logs.","Identify the failing step before proposing a fix."]}
    if workflow == "action_required":
        return {"classification":"action_required","question":"Would you like to inspect the workflow requirements?","actions":["Review the workflow run for required actions."]}
    if workflow in ("queued","in_progress"):
        return {"classification":"pending","question":"Would you like to check the run again after completion?","actions":["Wait for a terminal workflow result before assessing success."]}
    if workflow == "success":
        return {"classification":"observed_workflow_success","question":"Would you like to review deployment or acceptance evidence?","actions":["Verify deployment and acceptance separately from CI."]}
    return {"classification":"unknown","question":"Which operational evidence should I inspect next?","actions":[]}
