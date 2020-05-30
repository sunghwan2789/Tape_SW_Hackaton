import logging
import sys
import threading
from typing import Iterable, List, Tuple

from pydub import AudioSegment

import profane_recognizer
import utils

input_file = sys.argv[1] if len(sys.argv) > 1 else "input/test2.mp4"


def transcribe_sequently(segment_time=30000) -> Iterable[Tuple[str, int, int, int]]:
    logger = logging.getLogger("transcribe")
    logger.setLevel(logging.DEBUG)

    logger.info("load audio from wav")
    entire_audio = AudioSegment.from_wav("extract_audio/all_extract_audio.wav")

    entire_audio_playtime = len(entire_audio)
    logger.info("audio playtime is %s", entire_audio_playtime)

    last_recognition_start = 0
    while True:
        logger.info(
            "divide from %s to %s",
            last_recognition_start,
            last_recognition_start + segment_time,
        )
        audio_divided = entire_audio[last_recognition_start:][:segment_time]

        profane_times = get_profane_time(audio_divided.raw_data, last_recognition_start)

        recognition_suceed = False
        for word, start, end, profane in profane_times:
            recognition_suceed = True

            yield (
                word,
                start,
                end,
                profane,
            )

            last_recognition_start = start

        if not recognition_suceed:
            last_recognition_start += segment_time - 2000

        if last_recognition_start + segment_time >= entire_audio_playtime:
            break


def get_profane_time(content: bytes, start_time: int):
    from api.speechtotext import transcribe_with_word_time_offsets

    word_and_startend_time = transcribe_with_word_time_offsets(content)

    for word, start, end in word_and_startend_time:
        yield (
            word,
            start_time + start * 1000,
            start_time + end * 1000,
            detect_mature_language(word),
        )

def detect_mature_language(word: str):
    with open("profane_word.txt", "r") as profane_word:
        defined_profane_word: List[str] = profane_word.read().split()

    return any(filter(lambda x: x >= 0.6, (len(word) / len(i) for i in defined_profane_word if word.find(i) != -1)))



if __name__ == "__main__":

    # 프로그램을 시작하기 전 tmp 데이터들을 삭제합니다.
    print("TEMP 데이터 삭제")
    utils.delete_all_data_files()

    # ffmpeg를 사용하여 입력된 비디오에서 오디오를 추출합니다.
    print("오디오 추출")
    utils.extract_audio_in_video(input_file)

    # ffmpeg를 사용하여 입력된 비디오에서 썸네일을 추출합니다.
    print("썸네일 추출")
    utils.extract_image_in_video(input_file)

    # 단어 프로세싱
    result: List[Tuple[int, int]] = []
    for transcribtion in transcribe_sequently(30000):
        print(transcribtion)
        word, start, end, mature = transcribtion
        if mature:
            result.append((start, end,))

    # 결과를 바탕으로 비프음 처리된 오디오를 생성합니다.
    print("오디오 생성")
    utils.generate_sound(result)

    # 처리된 오디오와 기존의 영상을 합찹니다.
    print("결과 생성")
    utils.combine_audio_and_video(input_file)

    print("성공!")
