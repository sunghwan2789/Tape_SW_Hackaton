import os
import tempfile
import unittest

from video_manager import VideoManager


class VideoManagerTest(unittest.TestCase):
    def test_can_extract_audio(self):
        manager = VideoManager(
            os.path.join(os.path.dirname(__file__), "input", "test1.mp4"),
        )
        _, audio = tempfile.mkstemp(".wav")

        extracted_audio = manager.extract_audio(audio)

        self.assertEqual(audio, extracted_audio)
        self.assertTrue(os.path.exists(extracted_audio))

        os.remove(audio)

    def test_can_extract_thumbnail(self):
        manager = VideoManager(
            os.path.join(os.path.dirname(__file__), "input", "test2.mp4"),
        )
        _, thumbnail = tempfile.mkstemp(".jpg")

        extracted_thumbnail = manager.extract_thumbnail(thumbnail)

        self.assertEqual(thumbnail, extracted_thumbnail)
        self.assertTrue(os.path.exists(extracted_thumbnail))

        os.remove(thumbnail)


if __name__ == "__main__":
    unittest.main()
