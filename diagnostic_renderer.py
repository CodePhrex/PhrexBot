"""Present existing diagnostic results without recalculating metrics."""
from brand import NAME, DIVISION, TAGLINE, EMOJI
from diagnostic_severity import report_state

def diagnostic_payload(report):
    if not isinstance(report,str) or not report.strip() or len(report)>12000:
        raise ValueError("Invalid diagnostic report")
    lines=report.splitlines()
    blocks=[
        {"type":"header","text":{"type":"plain_text","text":NAME.upper()+" | Execution Intelligence"}},
        {"type":"context","elements":[{"type":"mrkdwn","text":EMOJI["ai"]+" *"+DIVISION+"* | "+TAGLINE}]},
        {"type":"divider"}
    ]
    def section(value):
        return {"type":"section","text":{"type":"plain_text","text":value}}
    emoji, label = report_state(report)
    blocks.append({"type":"context","elements":[{"type":"mrkdwn","text":EMOJI[emoji]+" *"+label+"*"}]})
    blocks.append(section(lines[0]))
    for line in lines[1:]:
        if not line.strip():
            continue
        for offset in range(0,len(line),2900):
            blocks.append(section(line[offset:offset+2900]))
    blocks.append({"type":"divider"})
    blocks.append({"type":"context","elements":[{"type":"plain_text","text":"Private report | Owner-scoped execution metadata"}]})
    if len(blocks)>50:
        blocks=[blocks[0],blocks[1],blocks[3]]+[section(report[i:i+2900]) for i in range(0,len(report),2900)]+[blocks[-1]]
    return {"text":report,"blocks":blocks,"response_type":"ephemeral"}
