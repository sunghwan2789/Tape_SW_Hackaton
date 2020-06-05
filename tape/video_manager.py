import pathlib
import subprocess
from typing import List, Tuple


class VideoManager(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.deferred_audio = None
        self.deferred_masks: List[Tuple[int, int, str]] = []

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

    def extract_thumbnail(self, output_filename: str = None) -> str:
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
                "00:00:00",
                # input file
                "-i",
                self.filename,
                # frame number
                "-vframes",
                "1",
                # audio null
                "-an",
                # size
                "-s",
                "1280x720",
                # output file
                output_filename,
            ],
        )
        completed_process.check_returncode()
        return output_filename

    def apply_mask(self, start_time, end_time):
        if not "detect_mask":
            self.deferred_masks.append([start_time, end_time, "mask"])

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
