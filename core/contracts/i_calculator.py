from abc import ABC, abstractmethod
from typing import Optional

class iCalculator(ABC):
    @staticmethod
    @abstractmethod
    def calculate_wpm(correct_chars, total_words: int, time_minutes: float) -> tuple:
        pass

    