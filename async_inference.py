"""Bounded asynchronous inference with private execution feedback."""
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore, Event, Thread, Lock
from time import monotonic
from uuid import uuid4
import requests
from execution_registry import ExecutionRegistry

registry = ExecutionRegistry()
from private_presentation import final_payload

_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="phrex-inference")
_slots = BoundedSemaphore(3)

def submit_inference(router, question, body, respond, audit):
    request_id = uuid4().hex[:12]
    accepted = monotonic()
    if not _slots.acquire(blocking=False):
        respond(text="Phrex intelligence queue is full. Please retry shortly.", response_type="ephemeral")
        return
    try:
        registry.remove_finished()
        registry.register(request_id, body.get('team_id'), body.get('user_id'))
    except Exception:
        _slots.release()
        respond(text='Request registration unavailable.', response_type='ephemeral')
        return
    def work():
        started = monotonic()
        done = Event()
        stage_lock = Lock()
        current = ['Processing intelligence']
        delivery_lock = Lock()
        remaining = 3
        def notify(message):
            nonlocal remaining
            with delivery_lock:
                if done.is_set() or remaining <= 0:
                    return
                remaining -= 1
                respond(text=message, response_type='ephemeral')
        def heartbeat():
            for interval in (15, 15, 30, 30):
                if done.wait(interval):
                    return
                with stage_lock:
                    stage = current[0]
                try:
                    notify(f':phrex-pending: *Still processing* | {stage} | Request `{request_id}` | Elapsed: {monotonic()-accepted:.1f}s')
                except Exception:
                    audit.warning('natural progress delivery unavailable')
                    return
        pulse = Thread(target=heartbeat, daemon=True, name='phrex-heartbeat')
        outcome = 'failed'
        try:
            registry.transition(request_id, 'executing')
            pulse.start()
            try:
                notify(f":phrex-ai: *Processing intelligence* | Request `{request_id}`\nAnalyzing your request. Queue wait: {started-accepted:.1f}s.")
            except Exception:
                audit.warning("natural progress delivery unavailable")
            def progress(stage):
                with stage_lock:
                    current[0] = stage
                try:
                    notify(f':phrex-ai: *{stage}* | Request `{request_id}` | Elapsed: {monotonic()-accepted:.1f}s')
                except Exception:
                    audit.warning('natural progress delivery unavailable')
            first_token = False
            def on_chunk(chunk):
                nonlocal first_token
                if not first_token:
                    first_token = True
                    registry.transition(request_id, 'generating')
                    progress('Generating response')
            try:
                answer = router.answer(question, body, progress=progress, on_chunk=on_chunk)
                outcome = 'completed'
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
            done.set()
            with delivery_lock:
                respond(**final_payload(answer, request_id, monotonic()-accepted))
        except Exception:
            outcome = 'failed'
            audit.warning("natural response delivery unavailable")
        finally:
            done.set()
            try:
                registry.transition(request_id, outcome)
            finally:
                _slots.release()
            audit.info("Inference elapsed seconds: %.2f", monotonic()-started)
    try:
        _pool.submit(work)
    except Exception:
        try:
            registry.transition(request_id, 'failed')
        finally:
            _slots.release()
        raise
