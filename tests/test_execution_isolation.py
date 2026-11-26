import unittest
from execution_registry import ExecutionRegistry
from execution_commands import execution_command
from retry_policy import RetryPolicy

class ExecutionIsolationTests(unittest.TestCase):
    def test_registry_and_commands(self):
        registry=ExecutionRegistry()
        rid="abcdef123456"
        registry.register(rid,"T1","U1")
        for team,user in (("T2","U1"),("T1","U2"),("T2","U2"),("*","U1"),("T1","*")):
            with self.assertRaises(PermissionError):
                registry.inspect(rid,team,user)
            with self.assertRaises(PermissionError):
                registry.cancel(rid,team,user)
            body={"team_id":team,"user_id":user}
            self.assertNotIn(rid,execution_command(registry,"queue",body))
            self.assertEqual(execution_command(registry,"cancel "+rid,body),"Request unavailable.")
        self.assertFalse(registry.inspect(rid,"T1","U1")["cancel_requested"])
        self.assertIn(rid,execution_command(registry,"queue",{"team_id":"T1","user_id":"U1"}))
        self.assertTrue(registry.cancel(rid,"T1","U1"))

    def test_retry_isolation(self):
        policy=RetryPolicy()
        rid="abcdef123456"
        self.assertTrue(policy.remember_failure(rid,"T1","U1","synthetic question"))
        for team,user in (("T2","U1"),("T1","U2"),("*","U1"),("T1","*")):
            with self.assertRaises(PermissionError):
                policy.reserve(rid,team,user)
        self.assertEqual(policy.reserve(rid,"T1","U1"),"synthetic question")
        with self.assertRaises(RuntimeError):
            policy.reserve(rid,"T1","U1")
        policy.finish(rid,True)
        with self.assertRaises(PermissionError):
            policy.reserve(rid,"T1","U1")

    def test_snapshot_isolation(self):
        registry=ExecutionRegistry()
        registry.register("abcdef123456","T1","U1")
        snapshot=registry.inspect("abcdef123456","T1","U1")
        snapshot["team"]="T2"
        registry.owned("T1","U1")[0][1]["state"]="completed"
        self.assertEqual(registry.inspect("abcdef123456","T1","U1")["state"],"queued")
        self.assertEqual(registry.owned("T2","U1"),[])
