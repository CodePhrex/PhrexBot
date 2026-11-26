import tempfile
import unittest
from pathlib import Path
from runtime_paths import data_root

class RuntimePathsTests(unittest.TestCase):
    def test_legacy(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(data_root({'LOCALAPPDATA': folder}), Path(folder) / 'CodePhrex' / 'Phrex')
    def test_explicit(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(data_root({'PHREX_DATA_ROOT': folder}), Path(folder).resolve())
    def test_invalid(self):
        for value in ('', 'relative'):
            with self.assertRaises(ValueError):
                data_root({'PHREX_DATA_ROOT': value})
