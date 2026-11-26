"""Local, in-memory charts; caller must authenticate workspace and owner."""
from execution_metrics import metrics
from visualizations import bar_chart

def execution_charts(path, team, owner, days=7):
    if not path.is_file():
        raise FileNotFoundError("Execution history unavailable")
    m=metrics(path,team,owner,days)
    period=f"Last {days} days; {m['total']} terminal executions"
    source="Owner-scoped execution history"
    charts={}
    charts["outcomes"]=bar_chart("Execution outcomes",list(m["outcomes"].items()),unit="requests",source=source,period=period)
    for key,title in (("queue_seconds","Queue latency"),("execution_seconds","Execution latency (includes delivery)")):
        values=m[key] or {}
        charts[key]=bar_chart(title,[(k,values.get(k)) for k in ("mean","median","p95","max")],unit="s",source=source,period=period)
    return charts
