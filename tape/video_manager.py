import logging
import subprocess
from typing import Any, List, Tuple

import settings
from api.vision import detect_mouths


class VideoManager(object):
    logger = logging.getLogger("VideoManager")

    def __init__(self, filename: str):
        self.filename = filename
        self.deferred_audio = None
        self.deferred_masks: List[Tuple[float, float, Any]] = []

    def extract_audio(self, output_filename: str = None) -> str:
        """Extract audio file from video.

        Args:
            output_filename: Output filename that the extracted audio goes to.

        Returns:
            Filename of the extracted audio.

        """

        completed_process = subprocess.run(
            [
                "ffmpeg",
                # loglevel
                "-v",
                "warning",
                # overwrite output
                "-y",
                # input file
                "-i",
                self.filename,
                # video null
                "-vn",
                # audio sampling rate
                "-ar",
                "44.1k",
                # audio channel
                "-ac",
                "1",
                # audio bitrate
                "-ab",
                "256k",
                # output file
                output_filename,
            ],
        )
        completed_process.check_returncode()
        return output_filename

    def extract_thumbnail(self, output_filename: str = None, time="00:00:00") -> str:
        """Extract thumbnail file from video.

        Args:
            output_filename: Output filename that the extracted thubmail goes to.

        Returns:
            Filename of the extracted thumbnail.

        """
        completed_process = subprocess.run(
            [
                "ffmpeg",
                # loglevel
                "-v",
                "warning",
                # overwrite output
                "-y",
                # thumbnail time
                "-ss",
                str(time),
                # input file
                "-i",
                self.filename,
                # frame number
                "-vframes",
                "1",
                # audio null
                "-an",
                # output file
                output_filename,
            ],
        )
        completed_process.check_returncode()
        return output_filename

    def apply_mask(self, start_time, end_time):
        return

        def generate_thumbnail():
            with open(
                self.extract_thumbnail(settings.ROOT / "output/t.jpg", start_time), "rb"
            ) as file:
                start_thumbnail = file.read()

            with open(
                self.extract_thumbnail(settings.ROOT / "output/t.jpg", end_time), "rb"
            ) as file:
                end_thumbnail = file.read()

            return (
                start_thumbnail,
                end_thumbnail,
            )

        start_mouths, end_mouths = [detect_mouths(i) for i in generate_thumbnail()]

        self.deferred_masks.append([start_time, end_time, start_mouths, end_mouths])

    def apply_audio(self, audio: str):
        self.deferred_audio = audio

    def save(self, filename: str):
        if self.deferred_audio:
            completed_process = subprocess.run(
                [
                    "ffmpeg",
                    # loglevel
                    "-v",
                    "warning",
                    # overwrite output
                    "-y",
                    # input video
                    "-i",
                    self.filename,
                    # filtered audio
                    "-i",
                    self.deferred_audio,
                    # video convert option
                    "-c:v",
                    "copy",
                    # audio convert option
                    "-c:a",
                    "aac",
                    # use input video
                    "-map",
                    "0:v",
                    # use filtered audio
                    "-map",
                    "1:a",
                    # output file
                    filename,
                ]
            )
            completed_process.check_returncode()
