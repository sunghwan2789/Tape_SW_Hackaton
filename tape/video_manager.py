import subprocess


class VideoManager(object):
    def __init__(self, filename: str):
        self.filename = filename

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
                "-y",
                "-i",
                self.filename,
                "-vn",
                "-ar",
                "44.1k",
                "-ac",
                "1",
                "-ab",
                "256k",
                output_filename,
            ],
        )
        completed_process.check_returncode()

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
                "-ss",
                "00:00:00",
                "-i",
                self.filename,
                "-y",
                "-vframes",
                "1",
                "-an",
                "-s",
                "1280x720",
                output_filename,
            ],
        )
        completed_process.check_returncode()
