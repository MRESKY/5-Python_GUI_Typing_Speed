import json
import os
from typing import Dict, Any

try:
    from .contracts.i_config import iConfig
except ImportError:
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from contracts.i_config import iConfig

class AppConfig(iConfig):
    def __init__(self, theme: str = "light"):
        self.theme = theme
        self._settings = self._load_default_settings()
        self.load_config()

        if theme:
            self._theme = theme

    def _load_default_settings(self) -> Dict[str, Any]:
        """Load default application settings"""
        return {
            "app_name": "Typing Speed Test",
            "Version": "1.0.0",
            "window":{
                "defult_size": [900,700],
                "min_size": [800,600],
                "resizeble": True,
            },
            "Themes": {
                "dark": {
                    "background": "#2b2b2b",
                    "surface": "#3c3c3c", 
                    "primary": "#4a9eff",
                    "secondary": "#6c757d",
                    "text": "#ffffff",
                    "text_secondary": "#cccccc",
                    "accent": "#17a2b8",
                    "success": "#28a745",
                    "warning": "#ffc107",
                    "error": "#dc3545",
                    "input_bg": "#404040",
                    "input_fg": "#ffffff",
                    "display_bg": "#363636",
                    "display_fg": "#e0e0e0",
                    "button_bg": "#4a9eff",
                    "button_fg": "#ffffff",
                    "button_hover": "#3a8eef"
                },
                "light": {
                    "background": "#ffffff",
                    "surface": "#f8f9fa",
                    "primary": "#007bff",
                    "secondary": "#6c757d", 
                    "text": "#212529",
                    "text_secondary": "#6c757d",
                    "accent": "#17a2b8",
                    "success": "#28a745",
                    "warning": "#ffc107",
                    "error": "#dc3545",
                    "input_bg": "#ffffff",
                    "input_fg": "#212529",
                    "display_bg": "#f8f9fa",
                    "display_fg": "#212529",
                    "button_bg": "#007bff",
                    "button_fg": "#ffffff",
                    "button_hover": "#0056b3"
                }
            },
            "fonts": {
                 "default": ("Arial", 12),
                "heading": ("Arial", 16, "bold"),
                "monospace": ("Courier New", 12),
                "large": ("Arial", 14),
                "small": ("Arial", 10)
            },
            "typing": {
                "default_duration": 60,
                "auto_start": False,
                "show_errors": True,
                "highlight_errors": True,
                "sound_enabled": False
            }
        }
    
    @property
    def APP_NAME(self) -> str:
        """Get application name"""
        return self._settings["app_name"]
    
    @property
    def VERSION(self) -> str:
        """Get application version"""
        return self._settings["Version"]
    
    @property
    def DEFAULT_SIZE(self) -> tuple:
        """Get default window size"""
        size = self._settings["window"]["defult_size"]
        return (size[0], size[1])
    
    @property
    def MIN_SIZE(self) -> tuple:
        """Get minimum window size"""
        size = self._settings["window"]["min_size"]
        return (size[0], size[1])
    
    def get_theme(self) -> str:
        """Get current theme name
        
        Return:
            str: Current theme(dark/light)
        """
        return self._theme
    
    def set_theme(self, theme:str) -> None:
        """
        Set application theme
        
        Args:
            theme: Theme name (dark/light)
        """

        if theme in self._settings["themes"]:
            self._theme = theme
            self.save_config()

    def get_available_themes(self) -> list:
        """
        Get list of available themes
        
        Returns:
            list: Available theme names
        """

        return list(self._settings["themes"].keys())
    
    def get_color(self, element: str) -> str:
        """
        Get color for UI element in current theme

        Args:
            element: UI element name (background, text, primmary, etc.)

        Returns:
            str: Hex color code
        """

        theme_colors = self._settings["theme"].get(self._theme, {})
        return theme_colors.get(element, "#000000")
