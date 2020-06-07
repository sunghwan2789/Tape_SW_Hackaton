from pathlib import Path

from pydub import AudioSegment

import settings


class AudioManager(object):
    beep_sound = AudioSegment.from_wav(settings.ROOT / "beep.wav",)

    def __init__(self, filename: str):
        self.filename = filename
        self.audio_segment = AudioSegment.from_wav(self.filename)

    @property
    def playtime(self):
        return len(self.audio_segment) / 1_000

    def slice(self, start_position, count):
        return self.audio_segment[start_position * 1_000 :][: count * 1_000]

    def apply_beep(self, start_time, end_time):
        self.audio_segment = (
            self.audio_segment[: start_time * 1_000]
            + self.beep_sound[: end_time * 1_000 - start_time * 1_000]
            + self.audio_segment[end_time * 1_000 :]
        )

    def save(self, filename: str):
        self.audio_segment.export(filename, format="mp3")
        return filename
