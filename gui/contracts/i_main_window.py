from abc import ABC, abstractmethod

class iMainWindow(ABC):
    @abstractmethod
    def setup_ui(self) -> None:
        pass

    @abstractmethod
    def update_wpm_display(self, wpm: float) -> None:
        pass

    @abstractmethod
    def update_accuracy_display(self, accuracy: float) -> None:
        pass

    @abstractmethod
    def show_time_remaining(self, time_seconds: float) -> None:
        pass