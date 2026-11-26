import logging
import unittest
from runtime_logging import EventFilter

class EventFilterTests(unittest.TestCase):
    def test_allowlist(self):
        def record(msg, args=()):
            return logging.LogRecord("phrex.audit", 20, "", 1, msg, args, None)
        gate = EventFilter()
        self.assertTrue(gate.filter(record("authorized command received")))
        self.assertFalse(gate.filter(record("arbitrary request body")))
        self.assertFalse(gate.filter(record("command denied", ("unexpected",))))
