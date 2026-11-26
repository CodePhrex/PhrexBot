import unittest
from execution_registry import ExecutionRegistry
from execution_commands import execution_command

class ControlTests(unittest.TestCase):
    def test_isolation(self):
        r=ExecutionRegistry()
        key="abcdef123456"
        r.register(key,"T","U")
        other={"team_id":"T","user_id":"V"}
        owner={"team_id":"T","user_id":"U"}
        self.assertNotIn(key,execution_command(r,"queue",other))
        self.assertIn(key,execution_command(r,"queue",owner))
        self.assertEqual("Request unavailable.",execution_command(r,"cancel "+key,other))
        self.assertIn("Cancellation requested",execution_command(r,"cancel "+key,owner))
        self.assertTrue(r.inspect(key,"T","U")["cancel_requested"])
