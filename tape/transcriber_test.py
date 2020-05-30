import os
import tempfile
import unittest

from audio_manager import AudioManager
from transcriber import Transcriber
from video_manager import VideoManager


class TranscriberTest(unittest.TestCase):
    def test_can_transcribe_long_speech(self):
        manager = VideoManager(
            os.path.join(os.path.dirname(__file__), "input", "test1.mp4"),
        )
        _, audio = tempfile.mkstemp(".wav")
        manager.extract_audio(audio)
        audio_manager = AudioManager(audio)

        transcriber = Transcriber(audio_manager)

        transcribe_result = list(transcriber.transcribe())

        self.assertGreaterEqual(len(transcribe_result), 1)


if __name__ == "__main__":
    unittest.main()
