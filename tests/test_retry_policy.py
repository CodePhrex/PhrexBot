import unittest
from retry_policy import RetryPolicy

class RetryTests(unittest.TestCase):
    def test_limits(self):
        p=RetryPolicy()
        self.assertTrue(p.remember_failure("id","T","U","question"))
        with self.assertRaises(PermissionError):
            p.reserve("id","T","V")
        self.assertEqual(p.reserve("id","T","U"),"question")
        with self.assertRaises(RuntimeError):
            p.reserve("id","T","U")
        p.finish("id",False)
        p.reserve("id","T","U")
        p.finish("id",False)
        with self.assertRaises(PermissionError):
            p.reserve("id","T","U")
