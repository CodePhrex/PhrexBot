import tempfile
import unittest
from pathlib import Path
from workspace_inventory import reconcile

class InventoryTests(unittest.TestCase):
    def test_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"inventory.db"
            row=dict(id="C12345678",name="old",archived=False,topic="",purpose="")
            snap=dict(team="T1",scope="Non-shared public channels visible to app",captured_at="2026-11-26T00:00:00Z",channels=[row],truncated=False)
            self.assertEqual(reconcile(path,snap,expected_team="T1")["changes"][0]["kind"],"newly_observed")
            row.update(name="new",archived=True,topic="updated")
            self.assertEqual([c["kind"] for c in reconcile(path,snap,expected_team="T1")["changes"]],["renamed","archived","metadata_changed"])
            self.assertEqual(reconcile(path,snap,expected_team="T1")["changes"],[])
            snap.update(channels=[],truncated=True)
            self.assertEqual(reconcile(path,snap,expected_team="T1")["not_observed"],[])
            snap["truncated"]=False
            self.assertEqual(reconcile(path,snap,expected_team="T1")["not_observed"],["C12345678"])
    def test_wrong_team(self):
        with self.assertRaises(PermissionError):
            reconcile("unused.db",{"team":"T2"},expected_team="T1")
