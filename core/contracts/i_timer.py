from abc import ABC, abstractmethod

class iTimer(ABC):
    @abstractmethod
    def start_timer(self) -> None:
        """Start the timer"""
        pass

    @abstractmethod
    def get_remaining_time(self) -> float:
        """Stop the timer"""
        pass

    @abstractmethod
    def is_time_up(self) -> bool:
        """Get elapsed time in seconds"""
        pass