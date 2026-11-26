import tempfile
import unittest
from pathlib import Path
from runtime_launcher import load_config

class RuntimeConfigTests(unittest.TestCase):
    def test_config(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / ".env"
            path.write_text("# comment\nPHREX_TEST= value=1 \ninvalid line\n", encoding="utf-8-sig")
            self.assertEqual(load_config(path, {"OTHER": "keep"}), {"OTHER": "keep", "PHREX_TEST": "value=1"})
