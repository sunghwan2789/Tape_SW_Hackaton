from typing import Iterable, Tuple

from google.cloud.speech_v1 import SpeechClient, enums, types


def transcribe_file_with_word_time_offsets(
    speech_file: str,
) -> Iterable[Tuple[str, float, float]]:
    """Recognize words with time offsets from a speech file.

    Args:
        speech_file: Filename of the speech file.

    Yields:
        The word with start time and end time that api recognized.

            [
                ('여기요', 0.0, 2.0),
                ('저기요', 3.6, 5.4),
                ('저', 5.4, 9.2),
                ('밖에서', 9.2, 9.6),
                ('장애인', 9.6, 10.0),
                ('주차', 10.0, 10.3),
                ('가능', 10.3, 10.5),
                ('까만색', 10.5, 11.3),
                ('소나타', 11.3, 11.7),
                ('글', 11.7, 11.8),
                ('찾아요', 11.8, 12.2),
                ('근데요', 12.2, 13.2)
            ]

    See:
        https://cloud.google.com/speech-to-text/docs/sync-recognize

    """
    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()
    yield from transcribe_with_word_time_offsets(content)


def transcribe_with_word_time_offsets(
    speech_content: bytes,
) -> Iterable[Tuple[str, float, float]]:
    """Recognize words with time offsets from a speech.

    Args:
        speech_content: Binary data of the speech.

    Yields:
        The word with start time and end time that api recognized.

            [
                ('여기요', 0.0, 2.0),
                ('저기요', 3.6, 5.4),
                ('저', 5.4, 9.2),
                ('밖에서', 9.2, 9.6),
                ('장애인', 9.6, 10.0),
                ('주차', 10.0, 10.3),
                ('가능', 10.3, 10.5),
                ('까만색', 10.5, 11.3),
                ('소나타', 11.3, 11.7),
                ('글', 11.7, 11.8),
                ('찾아요', 11.8, 12.2),
                ('근데요', 12.2, 13.2)
            ]

    See:
        https://cloud.google.com/speech-to-text/docs/sync-recognize

    """
    client = SpeechClient()

    audio = types.RecognitionAudio(content=speech_content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ko-KR",
        enable_word_time_offsets=True,
    )

    response = client.recognize(config, audio)

    for result in response.results:
        alternative = result.alternatives[0]

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            yield (
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9,
            )
