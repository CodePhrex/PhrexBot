import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('verify_wrapper', Path(__file__).resolve().parents[1] / 'deploy/windows/verify_wrapper.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class WrapperTests(unittest.TestCase):
    def test_match_and_mismatch(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'fixture.bin'
            path.write_bytes(b'fixture')
            self.assertTrue(module.verify_wrapper(path, hashlib.sha256(b'fixture').hexdigest()))
            self.assertFalse(module.verify_wrapper(path, '0' * 64))
    def test_invalid_digest(self):
        with self.assertRaises(ValueError):
            module.verify_wrapper('unused', 'invalid')
