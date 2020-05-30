import os

from pydub import AudioSegment


class AudioManager(object):
    beep_sound = AudioSegment.from_wav(
        os.path.join(os.path.dirname(__file__), "beep.wav"),
    )

    def __init__(self, filename: str):
        self.filename = filename
        self.audio_segment = AudioSegment.from_wav(self.filename)

    @property
    def playtime(self):
        return len(self.audio_segment)

    def slice(self, start_position, count):
        return self.audio_segment[start_position:][:count]

    def apply_beep(self, start_time, end_time):
        self.audio_segment = (
            self.audio_segment[:start_time]
            + self.beep_sound[: end_time - start_time]
            + self.audio_segment[end_time:]
        )

    def save(self, filename: str):
        self.audio_segment.export(filename, format="mp3")
        return filename
