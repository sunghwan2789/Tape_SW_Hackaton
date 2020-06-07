from typing import List, Tuple

import settings
from api.speechtotext import transcribe_file_with_word_time_offsets


def detect_mature_word(word: str):
    with open(settings.ROOT / "profane_word.txt", "r") as profane_word:
        defined_profane_word: List[str] = profane_word.read().split()

    return any(
        filter(
            lambda x: x >= 0.6,
            (len(word) / len(i) for i in defined_profane_word if word.find(i) != -1),
        )
    )
