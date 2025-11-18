import tkinter as tk
from gui.config import AppConfig
from gui.contracts.i_main_window import iMainWindow
from core.calculator import Calculator
from core.text_manager import TextManager
from core.timer import Timer

class MenuBar(tk.Menu):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_menus()

    def create_menus(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        self.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.add_cascade(label="Help", menu=help_menu)

    def new_file(self):
        pass

    def open_file(self):
        pass

    def exit_app(self):
        pass

    def show_about(self):
        pass


class BaseWindow(tk.Tk):
    def __init__(self, config: AppConfig = None, menu_bar: MenuBar = None):
        super().__init__()
        self.geometry(f'{config.DEFAULT_SIZE[0]}x{config.DEFAULT_SIZE[1]}')
        self.config = config
        self.menu_bar = menu_bar



class MainWindow(BaseWindow, iMainWindow):
    def __init__(self, config: AppConfig = None, Calculator: Calculator = None, TextManager: TextManager = None, Timer: Timer = None):
        super().__init__(config=config)
        self.calculator = Calculator
        self.text_manager = TextManager
        self.timer = Timer

    def setup_ui(self) -> None:
        self.title("Typing Speed Test")
        self.configure(bg=self.config.get_color('background'))
        
    def update_wpm_display(self, wpm: float) -> None:
        pass
    def update_accuracy_display(self, accuracy: float) -> None:
        pass
    def show_time_remaining(self, time_seconds: float) -> None:
        pass

if __name__ == "__main__":
    app_config = AppConfig(theme="dark")
    app = MainWindow(config=app_config, Calculator=Calculator, TextManager=TextManager, Timer=Timer)
    app.setup_ui()
    app.mainloop()