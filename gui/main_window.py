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
        # File Menu
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="New Test", command=self.callbacks.get('new_file', self.default_new_file))
        file_menu.add_command(label="Load Text", command=self.callbacks.get('open_file', self.default_open_file))
        file_menu.add_separator()
        file_menu.add_command(label="Save Results", command=self.callbacks.get('save_results', self.default_save))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.callbacks.get('exit_app', self.default_exit))
        self.add_cascade(label="File", menu=file_menu)

        # Settings Menu
        settings_menu = tk.Menu(self, tearoff=0)
        settings_menu.add_command(label="Preferences", command=self.callbacks.get('open_preferences', self.default_preferences))
        settings_menu.add_command(label="Themes", command=self.callbacks.get('change_theme', self.default_themes))
        self.add_cascade(label="Settings", menu=settings_menu)

        # Help Menu
        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="About", command=self.callbacks.get('show_about', self.default_about))
        self.add_cascade(label="Help", menu=help_menu)

    def default_new_file(self):
        messagebox.showinfo("New", "New file functionality not implemented")

    def default_open_file(self):
        messagebox.showinfo("Open", "Open file functionality not implemented")
    
    def default_save(self):
        messagebox.showinfo("Save", "Save functionality not implemented")
    
    def default_preferences(self):
        messagebox.showinfo("Preferences", "Preferences functionality not implemented")
    
    def default_themes(self):
        messagebox.showinfo("Themes", "Themes functionality not implemented")

    def default_exit(self):
        self.master.quit()

    def default_about(self):
        messagebox.showinfo("About", "Typing Speed Test v1.0")

class BaseWindow(tk.Tk):
    def __init__(self, config: AppConfig = None, menu_bar: MenuBar = None, dependencies: dict = None):
        super().__init__()

        self.app_config = config or AppConfig()
        self.dependencies = dependencies or {}
        

        self.geometry(f'{self.app_config.DEFAULT_SIZE[0]}x{self.app_config.DEFAULT_SIZE[1]}')
        self.title(self.app_config.APP_NAME)

        if menu_bar:
            self.menu_bar = menu_bar
        else:
            menu_callbacks = {
                'new_file': self.dependencies.get('new_file_callback'),
                'open_file': self.dependencies.get('open_file_callback'),
                'save_results': self.dependencies.get('save_results_callback'),
                'exit_app': self.dependencies.get('exit_app_callback'),
                'open_preferences': self.dependencies.get('open_preferences_callback'),
                'change_theme': self.dependencies.get('change_theme_callback'),
                'show_about': self.dependencies.get('show_about_callback')
            }
            self.menu_bar = MenuBar(master=self, callbacks=menu_callbacks)
        
        self.config(menu=self.menu_bar)

class MainWindow(BaseWindow, iMainWindow):
    def __init__(self, config: AppConfig = None, calculator: Calculator = None, text_manager: TextManager = None, timer: Timer = None):
        super().__init__(config=config)
        self.calculator = calculator
        self.text_manager = text_manager
        self.timer = timer

    def setup_ui(self) -> None:
        self.title("Typing Speed Test")
        self.configure(bg=self.app_config.get_color('background'))

    def update_wpm_display(self, wpm: float) -> None:
        pass
    def update_accuracy_display(self, accuracy: float) -> None:
        pass
    def show_time_remaining(self, time_seconds: float) -> None:
        pass

if __name__ == "__main__":
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Pack my box with five dozen liquor jugs.",
        "How vexingly quick daft zebras jump!"
    ]

    app_config = AppConfig(theme="dark")
    app = MainWindow(config=app_config, calculator=Calculator(), text_manager=TextManager(texts=texts), timer=Timer())
    app.setup_ui()
    app.mainloop()
