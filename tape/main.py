import json
import logging
import logging.config
import os
import sys

from audio_manager import AudioManager
from profane_recognizer import detect_mature_word
from transcriber import Transcriber
from video_manager import VideoManager

with open(os.path.join(os.path.dirname(__file__), "logger.json")) as config:
    logging.config.dictConfig(json.load(config))

input_file = sys.argv[1] if len(sys.argv) > 1 else "input/test2.mp4"


def main():
    logger = logging.getLogger()

    logger.info("start processing %s", input_file)

    manager = VideoManager(input_file)
    audio = manager.extract_audio("output/a.wav")
    thumbnail = manager.extract_thumbnail("output/a.jpg")

    audio_manager = AudioManager(audio)
    transcriber = Transcriber(audio_manager)

    for transcribtion in transcriber.transcribe():
        print(transcribtion)
        word, start, end = transcribtion
        if detect_mature_word(word):
            audio_manager.apply_beep(start, end)
            manager.apply_mask(start, end)

    manager.apply_audio(audio_manager.save("output/a_beep.wav"))
    manager.save("output/a.mp4")


if __name__ == "__main__":
    main()
