import unittest
from security import EventGate

class SecurityTests(unittest.TestCase):
    def test_replay_and_rate(self):
        now=[0]
        gate=EventGate(clock=lambda:now[0])
        self.assertTrue(gate.admit('E1','U1'))
        self.assertFalse(gate.admit('E1','U2'))
        self.assertFalse(gate.admit('E2','U1'))
        now[0]=16
        self.assertTrue(gate.admit('E2','U1'))
        self.assertFalse(gate.admit('E1','U2'))
        now[0]=601
        self.assertTrue(gate.admit('E1','U2'))
    def test_capacity(self):
        gate=EventGate(capacity=1)
        self.assertFalse(gate.admit(None,'U1'))
        self.assertTrue(gate.admit('E1','U1'))
        self.assertFalse(gate.admit('E2','U2'))
