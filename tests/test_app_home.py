import unittest
from app_home import build_home

class AppHomeTests(unittest.TestCase):
    def test_member(self):
        view=build_home(team="T1",expected_team="T1",user="U2",administrators={"U1"})
        self.assertEqual(view["type"],"home")
        self.assertNotIn("/phrex dashboard",str(view))
    def test_admin(self):
        view=build_home(team="T1",expected_team="T1",user="U1",administrators={"U1"})
        self.assertIn("/phrex dashboard",str(view))
        self.assertLess(len(view["blocks"]),100)
    def test_wrong_team(self):
        with self.assertRaises(PermissionError):
            build_home(team="T2",expected_team="T1",user="U1",administrators={"U1"})
