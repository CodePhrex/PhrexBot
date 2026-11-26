"""Acceptance evidence evaluation; never performs deployment."""
GATES=("runtime","security","identity","formatting","links","graphics","charts","memory","workspace","reconciliation","slack_knowledge","recommendations","app_home","ingestion","integration")

def evaluate(evidence):
    results={}
    for gate in GATES:
        record=evidence.get(gate)
        passed=isinstance(record,dict) and record.get("passed") is True and all(isinstance(record.get(k),str) and record[k].strip() for k in ("revision","test_reference","deployment_reference","live_reference","reviewer"))
        results[gate]="recorded_pass" if passed else "pending"
    revisions={evidence[g]["revision"] for g in GATES if results[g]=="recorded_pass"}
    return {"gates":results,"all_evidence_recorded":all(v=="recorded_pass" for v in results.values()) and len(revisions)==1,"scope":"Caller-supplied evidence completeness only; independent verification required"}
