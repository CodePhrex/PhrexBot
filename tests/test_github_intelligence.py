import unittest
from unittest.mock import Mock
from github_intelligence import GitHubIntelligence

class GitHubIntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.api = GitHubIntelligence('test', session=self.session)
    def response(self, data, status=200):
        r = Mock(status_code=status)
        r.json.return_value = data
        return r
    def test_inventory(self):
        own = {'name':'DroidLab','owner':{'login':'CodePhrex'}}
        other = {'name':'Other','owner':{'login':'other'}}
        self.session.get.side_effect = [self.response([other]*100), self.response([own])]
        result = self.api.repositories()
        self.assertEqual(result['repositories'],[own])
        self.assertFalse(result['truncated'])
        self.assertEqual(self.session.get.call_count,2)
    def test_limit(self):
        self.session.get.return_value = self.response([{}]*100)
        self.assertTrue(self.api.repositories(1)['truncated'])
    def test_activity(self):
        self.session.get.return_value = self.response([{'number':1},{'pull_request':{}}])
        self.assertEqual(self.api.activity('DroidLab','issues')['data'],[{'number':1}])
        with self.assertRaises(ValueError):
            self.api.activity('../secret','commits')
        with self.assertRaises(ValueError):
            self.api.activity('DroidLab','delete')
    def test_failure(self):
        self.session.get.return_value = self.response({},403)
        with self.assertRaisesRegex(RuntimeError,'403'):
            self.api.repositories()
