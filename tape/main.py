import json
import logging
import logging.config
import os
import sys

import settings
from audio_manager import AudioManager
from profane_recognizer import detect_mature_word
from transcriber import Transcriber
from video_manager import VideoManager

with open(settings.ROOT / "logger.json") as config:
    logging.config.dictConfig(json.load(config))

input_file = sys.argv[1] if len(sys.argv) > 1 else settings.ROOT / "input/test2.mp4"


def main():
    logger = logging.getLogger()

    logger.info("start processing %s", input_file)

    manager = VideoManager(input_file)
    audio = manager.extract_audio(settings.ROOT / "output/a.wav")
    thumbnail = manager.extract_thumbnail(settings.ROOT / "output/a.jpg")

    audio_manager = AudioManager(audio)
    transcriber = Transcriber(audio_manager)

    filter_sections = []

    for transcribtion in transcriber.transcribe():
        logger.debug("transcription: %s", transcribtion)
        word, start, end = transcribtion
        if detect_mature_word(word):
            logger.debug("mature word: %s, %s", word, detect_mature_word(word))
            audio_manager.apply_beep(start, end)
            manager.apply_mask(start, end)
            filter_sections.append({"start_time": start, "end_time": end, "word": word})

    manager.apply_audio(audio_manager.save(settings.ROOT / "output/a_beep.wav"))
    manager.save(settings.ROOT / "output/a.mp4")

    print(
        json.dumps(
            {
                "thumbnail": str(thumbnail),
                "filter_sections": filter_sections,
                "filter_video": str(settings.ROOT / "output" / "a.mp4"),
            }
        )
    )


if __name__ == "__main__":
    main()
