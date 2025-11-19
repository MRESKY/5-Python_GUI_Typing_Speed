from typing import Dict, Tuple, Final
from gui.contracts.i_config import IConfig


class AppConfig(IConfig):
    DEFAULT_COLOR: Final[str] = "#000000"
    DEFAULT_FONT_NAME: Final[str] = "default"
    DEFAULT_FONT_SIZE: Final[int] = 12
    DEFAULT_SIZE: Final[Tuple[int, int]] = (400, 400)
    DEFAULT_SIZE_WINDOW: Final[Dict[str, Tuple[int, int]]] = {
            'small': (100, 100),
            'medium': (400, 400),
            'large': (800, 800)
        }

    def __init__(self, theme: str = "light"):
        self._theme = theme
        self.colors = self._load_colors(theme)
        self.fonts = self._load_fonts()
        self.APP_NAME: Final[str] = "Typing Speed Test"

    def _load_colors(self, theme: str) -> Dict[str, str]:
        if theme == "dark":
            return {
                'primary': '#2E3440',
                'secondary': '#3B4252',
                'accent': '#5E81AC',
                'background': '#2E3440',
                'surface': '#3B4252',
                'text': '#ECEFF4',
                'text_secondary': '#D8DEE9',
                'success': '#A3BE8C',
                'warning': '#EBCB8B',
                'error': '#BF616A'
            }
        else:  # light
            return {
                'primary': '#ECEFF4',
                'secondary': '#D8DEE9',
                'accent': '#5E81AC',
                'background': '#FFFFFF',
                'surface': '#F8F9FA',
                'text': '#2E3440',
                'text_secondary': '#4C566A',
                'success': '#A3BE8C',
                'warning': '#EBCB8B',
                'error': '#BF616A'
            }

    def _load_fonts(self) -> Dict[str, Tuple]:
        return {
            'default': ("Segoe UI", 12),
            'heading': ("Segoe UI", 20, "bold"),
            'subheading': ("Segoe UI", 16, "bold"),
            'body': ("Segoe UI", 12),
            'caption': ("Segoe UI", 10, "italic")
        }

    def get_color(self, name: str) -> str:
        return self.colors.get(name, self.DEFAULT_COLOR)

    def get_font(self, name: str) -> Tuple:
        return self.fonts.get(name, self.fonts["default"])

    def switch_theme(self, theme_name: str) -> None:
        self._theme = theme_name
        self.colors = self._load_colors(theme_name)

    def get_size_window(self, name: str) -> tuple[int, int]:
        return self.DEFAULT_SIZE_WINDOW.get(name, self.DEFAULT_SIZE)
