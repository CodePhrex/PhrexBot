import unittest
from unittest.mock import patch
from natural import NaturalRouter,is_natural

class NaturalTests(unittest.TestCase):
    def test_routing(self):
        self.assertTrue(is_natural('Hello, how are you?'))
        self.assertFalse(is_natural('status droidlab'))
        self.assertTrue(is_natural('status of my projects'))
    def test_denial(self):
        with patch('natural.LocalIntelligence') as ai:
            r=NaturalRouter('local','T',{'U'},{},'token',None)
            with self.assertRaises(PermissionError):
                r.answer('hello',{'team_id':'T','user_id':'OTHER'})
            ai.return_value.answer.assert_not_called()
