import time
from core.contracts.i_timer import iTimer


class Timer(iTimer):
    def __init__(self, duration=int):
        self.start_time = None
        self.duration = duration

    def start(self):
        """Start the timer."""
        self.start_time = time.time()

    def remaining_time(self):
        """Return the remaining time in seconds."""
        if self.start_time is None:
            return self.duration
        elapsed = time.time() - self.start_time
        remaining = self.duration - elapsed
        return max(0, remaining)
    
    def is_time_up(self):
        """Check if the time is up."""
        return self.remaining_time() <= 0
    
if __name__ == "__main__":
    timer = Timer(duration=10)
    timer.start()
    print(f'Timer started for {timer.duration} seconds.')
    
    while not timer.is_time_up():
        print(f"Remaining time: {timer.remaining_time():.0f} seconds", end='\r')
        time.sleep(1)
    
    print("\nTime's up!")