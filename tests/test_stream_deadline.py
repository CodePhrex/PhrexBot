import unittest
from unittest.mock import patch
from streaming import collect_stream

class StreamDeadlineTests(unittest.TestCase):
    def test_empty_frames_cannot_bypass_deadline(self):
        with patch("streaming.monotonic",side_effect=[1,2,3]):
            with self.assertRaises(TimeoutError):
                collect_stream([b"",b"",b""],deadline=3)

    def test_late_terminal_frame_rejected(self):
        with patch("streaming.monotonic",return_value=10):
            with self.assertRaises(TimeoutError):
                collect_stream([b'{"message":{"content":"late"},"done":true}'],deadline=10)

    def test_timely_response(self):
        with patch("streaming.monotonic",return_value=1):
            self.assertEqual(collect_stream([b'{"message":{"content":"ok"},"done":true}'],deadline=2),"ok")
