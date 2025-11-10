from abc import ABC, abstractmethod

class iTimer(ABC):
    @abstractmethod
    def start_timer(self) -> None:
        pass

    @abstractmethod
    def get_remaining_time(self) -> float:
        pass

    @abstractmethod
    def is_time_up(self) -> bool:
        pass