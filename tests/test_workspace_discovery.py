import unittest
from unittest.mock import Mock
from workspace_discovery import discover_workspace, discover_emojis

class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.client=Mock()
        self.client.auth_test.return_value={"ok":True,"team_id":"T1"}
        self.scope=dict(team="T1",expected_team="T1",user="U1",administrators={"U1"})
    def test_channels(self):
        self.client.conversations_list.side_effect=[
            {"ok":True,"channels":[{"id":"C12345678","name":"general"},{"id":"C87654321","is_private":True}],"response_metadata":{"next_cursor":"next"}},
            {"ok":True,"channels":[{"id":"C12345679","name":"archived","is_archived":True}]}
        ]
        result=discover_workspace(self.client,**self.scope)
        self.assertEqual(len(result["channels"]),2)
        self.assertFalse(result["truncated"])
        self.assertTrue(result["channels"][1]["archived"])
    def test_denial(self):
        self.client.auth_test.return_value={"ok":True,"team_id":"T2"}
        with self.assertRaises(PermissionError):
            discover_workspace(self.client,**self.scope)
        self.client.conversations_list.assert_not_called()
    def test_emojis(self):
        self.client.emoji_list.return_value={"ok":True,"emoji":{"phrex-ai":"https://example.com/image.png"}}
        self.assertEqual(discover_emojis(self.client,**self.scope)["names"],["phrex-ai"])
