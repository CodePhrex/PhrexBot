import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from retry_policy import RetryPolicy
from execution_registry import ExecutionRegistry

class ExecutionRaceTests(unittest.TestCase):
    def test_retry_reservation_race(self):
        policy=RetryPolicy()
        rid="abcdef123456"
        self.assertTrue(policy.remember_failure(rid,"T1","U1","synthetic"))
        gate=Barrier(8,timeout=5)
        def reserve():
            gate.wait()
            try:
                return policy.reserve(rid,"T1","U1")
            except RuntimeError:
                return None
        with ThreadPoolExecutor(max_workers=8) as pool:
            results=list(pool.map(lambda _:reserve(),range(8)))
        self.assertEqual(results.count("synthetic"),1)
        self.assertEqual(results.count(None),7)
        policy.rollback(rid)
        self.assertEqual(policy.reserve(rid,"T1","U1"),"synthetic")
        policy.finish(rid,False)
        self.assertEqual(policy.reserve(rid,"T1","U1"),"synthetic")
        policy.finish(rid,False)
        with self.assertRaises(PermissionError):
            policy.reserve(rid,"T1","U1")

    def test_competing_terminal_transitions(self):
        registry=ExecutionRegistry()
        rid="abcdef123456"
        registry.register(rid,"T1","U1")
        registry.transition(rid,"executing")
        gate=Barrier(2,timeout=5)
        def finish(state):
            gate.wait()
            try:
                registry.transition(rid,state)
                return state
            except ValueError:
                return None
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(finish,("completed","cancelled")))
        self.assertEqual(results.count(None),1)
        winner=next(x for x in results if x is not None)
        self.assertEqual(registry.inspect(rid,"T1","U1")["state"],winner)
        self.assertFalse(registry.cancel(rid,"T1","U1"))
