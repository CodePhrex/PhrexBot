import unittest
from streaming import collect_stream

class StreamTests(unittest.TestCase):
    def test_complete(self):
        chunks = []
        self.assertEqual(collect_stream([b'{"message":{"content":"Hello "}}', b'{"message":{"content":"world"},"done":true}'], chunks.append), "Hello world")
        self.assertEqual(chunks, ["Hello ", "world"])

    def test_incomplete(self):
        with self.assertRaises(RuntimeError):
            collect_stream([b'{"message":{"content":"partial"}}'])

    def test_error(self):
        with self.assertRaises(RuntimeError):
            collect_stream([b'{"error":"failed"}'])

    def test_limit(self):
        with self.assertRaises(ValueError):
            collect_stream([b'{"message":{"content":"hello"},"done":true}'], limit=3)
