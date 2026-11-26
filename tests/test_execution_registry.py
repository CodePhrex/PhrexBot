import unittest
from execution_registry import ExecutionRegistry

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.r = ExecutionRegistry(1)
        self.r.register("id","team","owner")

    def test_owner(self):
        with self.assertRaises(PermissionError):
            self.r.cancel("id","team","other")
        self.assertTrue(self.r.cancel("id","team","owner"))
        self.assertTrue(self.r.inspect("id","team","owner")["cancel_requested"])

    def test_capacity(self):
        with self.assertRaises(RuntimeError):
            self.r.register("other","team","owner")

    def test_lifecycle(self):
        with self.assertRaises(ValueError):
            self.r.transition("id","completed")
        self.r.transition("id","executing")
        self.r.transition("id","completed")
        self.assertFalse(self.r.cancel("id","team","owner"))
        self.r.remove_finished()
        self.r.register("new","team","owner")
