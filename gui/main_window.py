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
        self.geometry(f'{self.app_config.DEFAULT_SIZE_WINDOW("large")[0]}x{self.app_config.DEFAULT_SIZE_WINDOW("large")[1]}')
