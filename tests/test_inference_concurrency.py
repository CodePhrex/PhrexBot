import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore, Event, Lock
from unittest.mock import patch, Mock
import async_inference as engine
from execution_registry import ExecutionRegistry
from queue_analytics import AdmissionWindow

class InferenceConcurrencyTests(unittest.TestCase):
    def test_capacity_and_recovery(self):
        entered, release = Event(), Event()
        lock = Lock()
        replies = []
        def respond(**payload):
            with lock:
                replies.append(payload)
        router = Mock()
        def answer(*args, **kwargs):
            entered.set()
            if not release.wait(5):
                raise RuntimeError("Test gate timed out")
            return "Synthetic answer"
        router.answer.side_effect = answer
        slots = BoundedSemaphore(3)
        registry = ExecutionRegistry()
        pool = ThreadPoolExecutor(max_workers=1)
        body = {"team_id":"T1","user_id":"U1"}
        with patch.multiple(engine,_pool=pool,_slots=slots,registry=registry,admissions=AdmissionWindow()), patch.object(engine,"record_execution"):
            try:
                engine.submit_inference(router,"synthetic",body,respond,Mock())
                self.assertTrue(entered.wait(3))
                with ThreadPoolExecutor(max_workers=8) as callers:
                    futures=[callers.submit(engine.submit_inference,router,"synthetic",body,respond,Mock()) for _ in range(7)]
                    for future in futures:
                        future.result(timeout=3)
                rows=registry.owned("T1","U1")
                self.assertEqual(len(rows),3)
                self.assertEqual(sum(r["state"]=="executing" for _,r in rows),1)
                self.assertEqual(sum(r["state"]=="queued" for _,r in rows),2)
                rejected=[p for p in replies if "queue is full" in p.get("text","")]
                self.assertEqual(len(rejected),5)
                self.assertTrue(all(p["response_type"]=="ephemeral" for p in rejected))
            finally:
                release.set()
                pool.shutdown(wait=True)
            self.assertEqual(router.answer.call_count,3)
            self.assertTrue(all(r["state"]=="completed" for _,r in registry.owned("T1","U1")))
            for _ in range(3):
                self.assertTrue(slots.acquire(blocking=False))
            self.assertFalse(slots.acquire(blocking=False))
            for _ in range(3):
                slots.release()
