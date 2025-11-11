# core/contracts/i_config.py
from typing import Protocol, Dict, Tuple

class IColorScheme(Protocol):
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text: str
    text_secondary: str
    success: str
    warning: str
    error: str


class IFontScheme(Protocol):
    default: Tuple[str, int]
    heading: Tuple[str, int, str]
    subheading: Tuple[str, int, str]
    body: Tuple[str, int]
    caption: Tuple[str, int]

class ISizeScheme(Protocol):
    small: int
    medium: int
    large: int


class IConfig(Protocol):
    COLORS: Dict[str, str]
    FONTS: Dict[str, Tuple]
    SIZES: Dict[str, int]
    THEME: str

    def get_color(self, name: str) -> str:
        ...

    def get_font(self, name: str) -> Tuple:
        ...

    def switch_theme(self, theme_name: str) -> None:
        ...

    def get_size_window(self, name: str) -> tuple[int, int]:
        ...