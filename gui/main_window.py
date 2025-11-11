import tkinter as tk
from config import AppConfig
from contracts.i_main_window import iMainWindow

class BaseWindow(tk.Tk):
    def __init__(self, config: AppConfig = None):
        super().__init__()
        self.geometry(f'{config.DEFAULT_SIZE[0]}x{config.DEFAULT_SIZE[1]}')
        self.config = config

class MainWindow(BaseWindow, iMainWindow):
    def __init__(self, config: AppConfig = None):
        super().__init__(config=config)
        self.title("Typing Speed Test")
        self.configure(bg=self.config.get_color('background'))
    def setup_ui(self) -> None:
        pass
    def update_wpm_display(self, wpm: float) -> None:
        pass
    def update_accuracy_display(self, accuracy: float) -> None:
        pass
    def show_time_remaining(self, time_seconds: float) -> None:
        pass

if __name__ == "__main__":
    app_config = AppConfig(theme="dark")
    app = MainWindow(config=app_config)
    app.setup_ui()
    app.mainloop()