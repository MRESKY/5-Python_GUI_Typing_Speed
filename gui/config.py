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
    def __init__(self, theme: str = "light", config_file: str = "config.json"):
        self.theme = theme
        self.config_file = config_file
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
                "default_size": [900,700],
                "min_size": [800,600],
                "resizable": True,
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
        size = self._settings["window"]["default_size"]
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

        if theme in self._settings["Themes"]:
            self._theme = theme
            self.save_config()

    def get_available_themes(self) -> list:
        """
        Get list of available themes
        
        Returns:
            list: Available theme names
        """

        return list(self._settings["Themes"].keys())
    
    def get_color(self, element: str) -> str:
        """
        Get color for UI element in current theme

        Args:
            element: UI element name (background, text, primmary, etc.)

        Returns:
            str: Hex color code
        """

        theme_colors = self._settings["Themes"].get(self._theme, {})
        return theme_colors.get(element, "#000000")
    
    def get_font(self, font_type: str) -> tuple:
        """
        Get font configuration for specified type
        
        Args:
            font_type: Font type name (default, heading, monospace, large, small)
            
        Returns:
            tuple: Font configuration (family, size, style)
        """
        fonts = self._settings.get("fonts", {})
        font_config = fonts.get(font_type, ("Arial", 12))
        
        # Ensure we return a tuple that can be used with tkinter
        if isinstance(font_config, list):
            return tuple(font_config)
        return font_config
    
    def load_config(self) -> bool:
        """ 
        Load configuration from file
        
        Returns:
            bool: True if config loaded successfully, False otherwise
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    saved_config = json.load(f)

                    # Merge saved config with default settings
                    self._merge_config(saved_config)

                    self._theme = saved_config.get("theme", self._theme)
                    return True
        except Exception as e:
            print(f"Error loading config: {e}")

        return False
    
    def save_config(self) -> bool:
        """
        Save current configuration to file
        
        Returns:
            bool: True if config saved successfully, False otherwise
        """
        try:
            config_to_save = {
                "theme": self._theme,
                "settings": self._settings
            }

            with open(self.config_file, "w") as f:
                json.dump(config_to_save, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
        
    def _merge_config(self, saved_config: Dict[str, Any]) -> None:
        """
        Merge saved configuration with default settings
        
        Args:
            saved_config: Saved configuration dictionary
        """
        def merge_dicts(default: Dict[str, Any], saved: Dict[str, Any]) -> Dict[str, Any]:
            for key, value in saved.items():
                if key in default and isinstance(value, dict) and isinstance(default[key], dict):
                    default[key] = merge_dicts(default[key], value)
                else:
                    default[key] = value
            return default
        
        if "settings" in saved_config:
            merge_dicts(self._settings, saved_config["settings"])
        
    def reset_to_defaults(self) -> None:
        """
        Reset configuration to default settings
        """
        self._settings = self._load_default_settings()
        self._theme = "light"
        self.save_config()
    
    def export_config(self, file_path: str) -> bool:
        """
        Export current configuration to specified file
        
        Args:
            file_path: Path to export config file
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            config_to_export = {
                "theme": self._theme,
                "settings": self._settings
            }

            with open(file_path, "w") as f:
                json.dump(config_to_export, f, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """
        Import configuration from specified file
        
        Args:
            file_path: Path to import config file

        Returns:
            bool: True if import successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False
            with open(file_path, "r") as f:
                imported_config = json.load(f)
            
            if "settings" in imported_config:
                self._merge_config(imported_config)
            
            if "theme" in imported_config:
                self._theme = imported_config["theme"]
            
            self.save_config()
            return True
        
        except Exception as e:
            print(f"Error importing config: {e}")
            return False