from abc import ABC, abstractmethod

class iConfig(ABC):
    @abstractmethod
    def get_color(self, element: str) -> str:
        """Get color for UI element"""
        pass

    @abstractmethod
    def get_theme(self) -> str:
        """Get current theme"""
        pass

    @abstractmethod
    def set_theme(self, theme: str) -> None:
        """Set theme"""
        pass