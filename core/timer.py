import time
from core.contracts.i_timer import iTimer
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)


class Timer(iTimer):
    def __init__(self, duration=int):
        self.start_time = None
        self.duration = duration

    def start_timer(self):
        """Start the timer."""
        self.start_time = time.time()

    def get_remaining_time(self):
        """Return the remaining time in seconds."""
        if self.start_time is None:
            return self.duration
        elapsed = time.time() - self.start_time
        remaining = self.duration - elapsed
        return max(0, remaining)
    
    def is_time_up(self):
        """Check if the time is up."""
        return self.get_remaining_time() <= 0
    
if __name__ == "__main__":
    timer = Timer(duration=10)
    timer.start_timer()
    print(f'Timer started for {timer.duration} seconds.')
    
    while not timer.is_time_up():
        print(f"Remaining time: {timer.get_remaining_time():.0f} seconds", end='\r')
        time.sleep(1)
    
    print("\nTime's up!")