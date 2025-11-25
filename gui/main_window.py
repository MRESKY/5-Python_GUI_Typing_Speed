import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
from typing import Dict

# Adjust sys.path to include project root for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Imports from best_practice modules
from gui.config import AppConfig
from gui.contracts.i_main_window import iMainWindow
from core.calculator import Calculator
from core.text_manager import TextManager
from core.timer import Timer

class MenuBar(tk.Menu):
    def __init__(self, master=None, callbacks: dict = None):
        super().__init__(master)
        self.master = master
        self.callbacks = callbacks or {}
        self.create_menus()

    def create_menus(self):
        """Create the menu bar with File and Help menus"""
        # File Menu
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="New Test", accelerator="Ctrl+N", 
                              command=self.callbacks.get('new_file', self.deafult_new_file))
        file_menu.add_command(label="Load Text", accelerator="Ctrl+O",
                              command=self.callbacks.get('load_file', self.default_load_file))
        file_menu.add_separator()
        file_menu.add_command(label="Save Results", accelerator="Ctrl+S",
                              command=self.callbacks.get('save_file', self.default_save_file))
        file_menu.add_command(label="Export Config",
                              command=self.callbacks.get('export_config', self.default_export_config))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q",
                                command=self.callbacks.get('exit_app', self.default_exit_app))
        self.add_cascade(label="File", menu=file_menu)

        # Setting Menu
        settings_menu = tk.Menu(self, tearoff=0)
        settings_menu.add_command(label="Preferences",
                                  command=self.callbacks.get('open_settings', self.default_open_settings))
        
        # Theme Submenu
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        theme_menu.add_command(label="Dark Theme", 
                                   command=lambda: self.callbacks.get('change_theme',lambda: None)('dark'))
        theme_menu.add_command(label="Light Theme",
                                   command=lambda: self.callbacks.get('change_theme',lambda: None)('light'))
        settings_menu.add_cascade(label="Theme", menu=theme_menu)
        self.add_cascade(label="Theme", menu=settings_menu)

        # Difficulty Submenu
        difficulty_menu = tk.Menu(settings_menu, tearoff=0)
        difficulty_menu.add_command(label="Easy",
                                        command=lambda: self.callbacks.get('change_difficulty',lambda: None)('easy'))
        difficulty_menu.add_command(label="Medium",
                                        command=lambda: self.callbacks.get('change_difficulty',lambda: None)('medium'))
        difficulty_menu.add_command(label="Hard",
                                        command=lambda: self.callbacks.get('change_difficulty',lambda: None)('hard'))
        difficulty_menu.add_command(label="Programming",
                                        command=lambda: self.callbacks.get('change_difficulty',lambda: None)('programming'))
        settings_menu.add_cascade(label="Difficulty", menu=difficulty_menu)

        self.add_cascade(label="Settings", menu=settings_menu)

        # Help Menu
        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="Instructions", accelerator="F1",
                              command=self.callbacks.get('show_instructions', self.default_show_instructions))
        help_menu.add_command(label="Statistics",
                              command=self.callbacks.get('show_statistics', self.default_show_statistics))
        help_menu.add_separator()
        help_menu.add_command(label="About",
                              command=self.callbacks.get('show_about', self.default_show_about))
        self.add_cascade(label="Help", menu=help_menu)

    def deafult_new_file(self):
        messagebox.showinfo("New Test", "New Test action triggered.")
    def default_load_file(self):
        messagebox.showinfo("Load Text", "Load Text action triggered.")
    def default_save_file(self):
        messagebox.showinfo("Save Results", "Save Results action triggered.")
    def default_export_config(self):
        messagebox.showinfo("Export Config", "Export Config action triggered.")
    def default_exit_app(self):
        messagebox.showinfo("Exit", "Exit action triggered.")
    def default_open_settings(self):
        messagebox.showinfo("Preferences", "Preferences action triggered.")
    def default_show_instructions(self):
        messagebox.showinfo("Instructions", "Instructions action triggered.")
    def default_show_statistics(self):
        messagebox.showinfo("Statistics", "Statistics action triggered.")
    def default_show_about(self):
        messagebox.showinfo("About", "About action triggered.")
    

class BaseWindow(tk.Tk, iMainWindow):
    def __init__(self, config: AppConfig = None, menu_bar: MenuBar = None, dependencies: Dict = None):
        super().__init__()
        self.app_config = config or AppConfig()
        self.dependencies = dependencies or {}

        # Set window properties
        self.geometry(f'{self.app_config.DEFAULT_SIZE[0]}x{self.app_config.DEFAULT_SIZE[1]}')
        self.minsize(self.app_config.MIN_SIZE[0], self.app_config.MIN_SIZE[1])
        self.title(self.app_config.APP_NAME)

        # Set menu bar
        if menu_bar:
            self.menu_bar = menu_bar
        else:
            menu_callbacks = {
                'new_file': self.dependencies.get('new_file_handler'),
                'load_file': self.dependencies.get('load_file_handler'),
                'save_file': self.dependencies.get('save_file_handler'),
                'export_config': self.dependencies.get('export_config_handler'),
                'exit_app': self.dependencies.get('exit_app_handler'),
                'open_settings': self.dependencies.get('open_settings_handler'),
                'change_theme': self.dependencies.get('change_theme_handler'),
                'change_difficulty': self.dependencies.get('change_difficulty_handler'),
                'show_instructions': self.dependencies.get('show_instructions_handler'),
                'show_statistics': self.dependencies.get('show_statistics_handler'),
                'show_about': self.dependencies.get('show_about_handler')
            }
            self.menu_bar = MenuBar(self, callbacks=menu_callbacks)

        # attach the menu bar to the window
        self.config(menu=self.menu_bar)

        # Setup keyboard shortcuts
        self.bind_all("<Control-n>", lambda event: self.dependencies.get('new_file_handler', lambda: None)())
        self.bind_all("<Control-o>", lambda event: self.dependencies.get('load_file_handler', lambda: None)())
        self.bind_all("<Control-s>", lambda event: self.dependencies.get('save_file_handler', lambda: None)())
        self.bind_all("<Control-q>", lambda event: self.dependencies.get('exit_app_handler', self.quit)())
        self.bind_all("<F1>", lambda event: self.dependencies.get('show_instructions_handler', lambda: None)())
    
class MainWindow(BaseWindow, iMainWindow):
    def __init__(self, config: AppConfig = None, menu_bar: MenuBar = None,
                 calculator: Calculator= None, text_manager: TextManager= None, timer: Timer=None):
        
        # Create dependencies dictionary
        dependencies = {
            "new_file_handler": self.handle_new_test,
            "load_file_handler": self.handle_load_text,
            "save_file_handler": self.handle_save_results,
            "export_config_handler": self.handle_export_config,
            "exit_app_handler": self.handle_exit_app,
            "open_settings_handler": self.handle_open_settings,
            "change_theme_handler": self.handle_change_theme,
            "change_difficulty_handler": self.handle_change_difficulty,
            "show_instructions_handler": self.handle_show_instructions,
            "show_statistics_handler": self.handle_show_statistics,
            "show_about_handler": self.handle_show_about,
        }
        
        # Initialize base window
        super().__init__(config, menu_bar, dependencies=dependencies)

        # inject core services
        self.calculator = calculator or Calculator()
        self.timer = timer or Timer()
        self.text_manager = text_manager or TextManager()

        