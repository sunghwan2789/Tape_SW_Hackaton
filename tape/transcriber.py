import logging
from typing import Iterable, Tuple

from pydub import AudioSegment

from api.speechtotext import transcribe_with_word_time_offsets
from audio_manager import AudioManager


class Transcriber(object):
    """Transcriber that uses a speech file."""

    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager
        self.logger = logging.getLogger(self.__class__.__name__)

    def transcribe(self, segment_time=60) -> Iterable[Tuple[str, int, int, int]]:
        self.logger.info("audio playtime is %s", self.audio_manager.playtime)

        last_recognition_start = 0
        while True:
            self.logger.info(
                "divide from %s to %s",
                last_recognition_start,
                last_recognition_start + segment_time,
            )
            audio_divided = self.audio_manager.slice(
                last_recognition_start, segment_time,
            )

            word_and_startend_time = transcribe_with_word_time_offsets(
                audio_divided.raw_data,
            )

            word_spoken = False
            new_recognition_start = last_recognition_start
            for word, start, end in word_and_startend_time:
                word_spoken = True

                yield (
                    word,
                    new_recognition_start + start,
                    new_recognition_start + end,
                )

                last_recognition_start = new_recognition_start + start

            if not word_spoken:
                last_recognition_start += segment_time - 2

            if last_recognition_start + segment_time >= self.audio_manager.playtime:
                break
