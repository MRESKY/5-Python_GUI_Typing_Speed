from abc import ABC, abstractmethod
from typing import List

class iTextManager(ABC):
    @abstractmethod
    def get_random_text(self) -> str:
        pass

    @abstractmethod
    def compare_texts(self, user_input: str) -> tuple[int, int]:
        pass