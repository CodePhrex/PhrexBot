import unittest
from log_stream import approved
class LogStreamTests(unittest.TestCase):
    def test_allowlist(self):
        prefix = "2026-11-26 05:30:06,097 INFO "
        self.assertTrue(approved(prefix + "Runtime launch requested"))
        self.assertTrue(approved(prefix + "authorized command received"))
        self.assertFalse(approved(prefix + "token=secret"))
        self.assertFalse(approved(prefix + "Runtime launch requested secret"))
    def test_rotation_and_duplicates(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        from log_stream import entries
        with TemporaryDirectory() as d:
            folder = Path(d)
            row = '2026-11-26 05:30:06,097 INFO Runtime launch requested'
            later = '2026-11-26 05:30:07,097 INFO Runtime exited with code 0'
            (folder / 'runtime.log.1').write_text(row + '\n')
            (folder / 'runtime.log').write_text(row + '\n' + later + '\n')
            self.assertEqual([r[2] for r in entries(folder)], [row, later])

    def test_checkpoint_replacement(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        import json
        from log_stream import save_checkpoint
        with TemporaryDirectory() as d:
            path = Path(d) / 'checkpoint.json'
            save_checkpoint(path, ('first', 'runtime.log', 'event'))
            save_checkpoint(path, ('second', 'runtime.log', 'event'))
            self.assertEqual(json.loads(path.read_text()), ['second', 'runtime.log', 'event'])
            self.assertFalse(path.with_suffix('.tmp').exists())

    def test_empty_checkpoint_is_durable(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        import json
        from log_stream import save_checkpoint, entries
        with TemporaryDirectory() as d:
            folder = Path(d)
            checkpoint = folder / "checkpoint.json"
            save_checkpoint(checkpoint, ("", "", ""))
            row = "2026-11-26 05:30:06,097 INFO Runtime launch requested"
            (folder / "runtime.log").write_text(row + "\n")
            previous = tuple(json.loads(checkpoint.read_text()))
            self.assertEqual(len([r for r in entries(folder) if r > previous]), 1)

    def test_privacy_failure_never_posts(self):
        from unittest.mock import Mock, patch
        from log_stream import start_log_stream
        for channel_info in (
            {"id": "C0CM8QC7601", "name": "phrex-logs", "is_private": False, "is_member": True},
            {"id": "C0CM8QC7601", "name": "phrex-logs", "is_private": True, "is_member": True, "is_ext_shared": True},
        ):
            client = Mock()
            client.auth_test.return_value = {"team_id": "T_TEST"}
            client.conversations_info.return_value = {"channel": channel_info}
            with patch.dict("os.environ", {"PHREX_LOG_CHANNEL": "C0CM8QC7601", "LOCALAPPDATA": "."}), patch("log_stream.threading.Thread") as thread:
                start_log_stream(client, "T_TEST")
                thread.call_args.kwargs["target"]()
            client.chat_postMessage.assert_not_called()

    def test_missing_privacy_permission_never_posts(self):
        from unittest.mock import Mock, patch
        from log_stream import start_log_stream
        client = Mock()
        client.auth_test.return_value = {"team_id": "T_TEST"}
        client.conversations_info.side_effect = RuntimeError("missing_scope")
        with patch.dict("os.environ", {"PHREX_LOG_CHANNEL": "C0CM8QC7601", "LOCALAPPDATA": "."}), patch("log_stream.threading.Thread") as thread, patch("log_stream.threading.Event") as event:
            event.return_value.is_set.side_effect = [False, True]
            start_log_stream(client, "T_TEST")
            thread.call_args.kwargs["target"]()
            event.return_value.wait.assert_called_once_with(30)
        client.chat_postMessage.assert_not_called()

    def test_rate_limit_retry_after(self):
        from unittest.mock import Mock, patch
        from log_stream import start_log_stream
        client = Mock()
        error = RuntimeError("rate limited")
        error.response = Mock(status_code=429, headers={"Retry-After": "47"})
        client.auth_test.side_effect = error
        with patch.dict("os.environ", {"PHREX_LOG_CHANNEL": "C0CM8QC7601", "LOCALAPPDATA": "."}), patch("log_stream.threading.Thread") as thread, patch("log_stream.threading.Event") as event:
            event.return_value.is_set.side_effect = [False, True]
            start_log_stream(client, "T_TEST")
            thread.call_args.kwargs["target"]()
            event.return_value.wait.assert_called_once_with(47)
        client.chat_postMessage.assert_not_called()
