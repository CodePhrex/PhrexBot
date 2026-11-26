import unittest
from access_policy import AccessPolicy, require_screened_text

class AccessPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy=AccessPolicy(team="T1",administrators={"U1","*"},members={"U2"})
    def test_roles(self):
        self.assertTrue(self.policy.permits(team="T1",user="U1",capability="host_read"))
        self.assertFalse(self.policy.permits(team="T1",user="U2",capability="host_read"))
        self.assertTrue(self.policy.permits(team="T1",user="U2",capability="help"))
    def test_default_deny(self):
        for team,user,cap in [("T2","U1","help"),("T1","*","help"),("T1","U3","help"),("T1","U1","shell_execute")]:
            self.assertFalse(self.policy.permits(team=team,user=user,capability=cap))
    def test_owner_isolation(self):
        with self.assertRaises(PermissionError):
            self.policy.require(team="T1",user="U1",capability="memory_read",owner="U2")
    def test_screening(self):
        for value in ["xoxb-example-token","GITHUB_TOKEN=example","-----BEGIN PRIVATE KEY-----"]:
            with self.assertRaises(ValueError):
                require_screened_text(value)
        self.assertEqual(require_screened_text("Project documentation"),"Project documentation")
