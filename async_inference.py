"""Bounded asynchronous slash-command inference."""
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore
from time import monotonic

_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="phrex-inference")
_slots = BoundedSemaphore(1)

def submit_inference(router, question, body, respond, audit):
    if not _slots.acquire(blocking=False):
        respond(text="Phrex is processing another intelligence request. Please retry shortly.", response_type="ephemeral")
        return
    def work():
        started = monotonic()
        try:
            try:
                answer = router.answer(question, body)
            except PermissionError:
                answer = "Administrator access required."
            except Exception:
                audit.warning("natural intelligence unavailable")
                answer = "Local intelligence unavailable. Check model and host."
            respond(text="Phrex intelligence", blocks=[{"type":"section","text":{"type":"plain_text","text":answer[:2900]}}], response_type="ephemeral")
        except Exception:
            audit.warning("natural response delivery unavailable")
        finally:
            audit.info("Inference elapsed seconds: %.2f", monotonic()-started)
            _slots.release()
    try:
        _pool.submit(work)
    except Exception:
        _slots.release()
        raise
