"""Private Slack response payloads; never publish partial operational content."""
def final_payload(answer, request_id, elapsed):
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("Missing answer")
    if len(answer) > 12000:
        raise ValueError("Answer exceeds limit")
    blocks = [{"type":"section","text":{"type":"plain_text","text":answer[i:i+2900]}} for i in range(0,len(answer),2900)]
    blocks.append({"type":"context","elements":[{"type":"plain_text","text":f"Request {request_id} | Elapsed: {elapsed:.1f}s"}]})
    return {"text":answer, "blocks":blocks, "response_type":"ephemeral"}
