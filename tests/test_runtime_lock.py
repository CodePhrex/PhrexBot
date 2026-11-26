import os
import tempfile
import unittest
from unittest.mock import patch
from runtime_lock import runtime_lock, AlreadyRunning

class RuntimeLockTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows lock")
    def test_exclusive_and_released(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {"LOCALAPPDATA": folder}):
            with runtime_lock():
                with self.assertRaises(AlreadyRunning):
                    with runtime_lock():
                        self.fail("duplicate admitted")
            with runtime_lock():
                pass
