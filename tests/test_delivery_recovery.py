import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore
from unittest.mock import Mock, patch
import async_inference as engine
from execution_registry import ExecutionRegistry
from queue_analytics import AdmissionWindow

class DeliveryRecoveryTests(unittest.TestCase):
    def test_final_delivery_failure_releases_capacity(self):
        registry=ExecutionRegistry()
        slots=BoundedSemaphore(3)
        pool=ThreadPoolExecutor(max_workers=1)
        router=Mock()
        router.answer.return_value="Synthetic answer"
        def respond(**payload):
            if "blocks" in payload:
                raise RuntimeError("Synthetic delivery failure")
        with patch.multiple(engine,registry=registry,_slots=slots,_pool=pool,admissions=AdmissionWindow()), patch.object(engine,"record_execution") as telemetry:
            try:
                engine.submit_inference(router,"synthetic",{"team_id":"T1","user_id":"U1"},respond,Mock())
            finally:
                pool.shutdown(wait=True)
            rows=registry.owned("T1","U1")
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0][1]["state"],"failed")
            telemetry.assert_called_once()
            self.assertEqual(telemetry.call_args.args[3],"failed")
            self.assertEqual(telemetry.call_args.args[-1],"delivery")
            for _ in range(3):
                self.assertTrue(slots.acquire(blocking=False))
            self.assertFalse(slots.acquire(blocking=False))
            for _ in range(3):
                slots.release()
