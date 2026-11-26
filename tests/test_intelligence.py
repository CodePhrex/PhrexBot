import unittest
from unittest.mock import Mock
from intelligence import LocalIntelligence

class IntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.ai = LocalIntelligence('test-model',self.session)
        self.auth = dict(user_id='U1',team_id='T1',expected_team='T1',administrators={'U1'})
    def test_denied(self):
        with self.assertRaises(PermissionError):
            self.ai.answer('status',{},**dict(self.auth,user_id='U2'))
        self.session.post.assert_not_called()
    def test_answer(self):
        self.session.post.return_value = Mock(status_code=200)
        self.session.post.return_value.json.return_value = {'message':{'content':'Evidence unavailable'}}
        self.assertEqual(self.ai.answer('status',{},**self.auth),'Evidence unavailable')
        self.assertEqual(self.session.post.call_args.args[0],'http://127.0.0.1:11434/api/chat')
        self.assertFalse(self.session.post.call_args.kwargs['allow_redirects'])
    def test_bounds(self):
        with self.assertRaises(ValueError):
            self.ai.answer('status',{'text':'x'*25000},**self.auth)
        self.session.post.assert_not_called()
    def test_failure(self):
        self.session.post.return_value = Mock(status_code=503)
        with self.assertRaises(RuntimeError):
            self.ai.answer('status',{},**self.auth)
