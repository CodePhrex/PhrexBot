"""Bounded asynchronous inference with private execution feedback."""
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore
from time import monotonic
from uuid import uuid4
import requests

_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="phrex-inference")
_slots = BoundedSemaphore(3)

def submit_inference(router, question, body, respond, audit):
    request_id = uuid4().hex[:12]
    accepted = monotonic()
    if not _slots.acquire(blocking=False):
        respond(text="Phrex intelligence queue is full. Please retry shortly.", response_type="ephemeral")
        return
    def work():
        started = monotonic()
        try:
            try:
                respond(text=f":phrex-ai: *Processing intelligence* | Request `{request_id}`\nAnalyzing your request. Queue wait: {started-accepted:.1f}s.", response_type="ephemeral")
            except Exception:
                audit.warning("natural progress delivery unavailable")
            try:
                answer = router.answer(question, body)
            except PermissionError:
                answer = "Administrator access required."
            except requests.exceptions.Timeout:
                audit.warning("natural intelligence unavailable")
                answer = "The local intelligence request timed out. Please retry with a narrower question."
            except requests.exceptions.ConnectionError:
                audit.warning("natural intelligence unavailable")
                answer = "The local intelligence service could not be reached. Check Ollama availability."
            except Exception:
                audit.warning("natural intelligence unavailable")
                answer = "Local intelligence unavailable. Check model and host."
            respond(text="Phrex intelligence", blocks=[{"type":"section","text":{"type":"plain_text","text":answer[:2900]}},{"type":"context","elements":[{"type":"mrkdwn","text":f"Request `{request_id}` | Elapsed: {monotonic()-accepted:.1f}s"}]}], response_type="ephemeral")
        except Exception:
            audit.warning("natural response delivery unavailable")
        finally:
            _slots.release()
            audit.info("Inference elapsed seconds: %.2f", monotonic()-started)
    try:
        _pool.submit(work)
    except Exception:
        _slots.release()
        raise
