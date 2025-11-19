"""
Timer module Implementation with Real-time Updates.
===================================================

This is the COMPLATE working version of the Timer class with all features:
- Real-time time tracking
- Start/stop/pause functionality  
- Callback system for UI updates
- Thread-safe implementation
"""

# Import
import time
import threading
import sys
import os

# Import
from typing import Callable, Optional
from core.contracts.i_timer import iTimer

# Adjust sys.path to include project root for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)


class Timer(iTimer):
    def __init__(self, duration: int = 60, callback: Optional[Callable[[float], None]] = None):
        self.duration = duration
        self.callback = callback
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.is_paused = False
        self.elapsed_paused_time = 0.0
        self._timer_thread = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start the timer"""
        if self.is_running:
            return
            
        self.start_time = time.time()
        self.end_time = None
        self.is_running = True
        self.is_paused = False
        self._stop_event.clear()
        
        # Start background thread for real-time updates
        if self.callback:
            self._timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
            self._timer_thread.start()

    def stop(self) -> None:
        """Stop the timer"""
        if not self.is_running:
            return
            
        self.end_time = time.time()
        self.is_running = False
        self.is_paused = False
        
        # Stop background thread
        if self._timer_thread:
            self._stop_event.set()
            self._timer_thread = None

    def pause(self) -> None:
        """Pause the timer"""
        if not self.is_running or self.is_paused:
            return
            
        self.is_paused = True
        self.elapsed_paused_time += time.time() - self.start_time

    def resume(self) -> None:
        """Resume the timer"""
        if not self.is_running or not self.is_paused:
            return
            
        self.start_time = time.time()
        self.is_paused = False

    def reset(self) -> None:
        """Reset the timer"""
        self.stop()
        self.start_time = None
        self.end_time = None
        self.elapsed_paused_time = 0.0

    def get_elapsed_time(self) -> float:
        """
        Get elapsed time in seconds
        
        Returns:
            float: Elapsed time in seconds
        """
        if not self.start_time:
            return 0.0
            
        if self.is_paused:
            return self.elapsed_paused_time
            
        current_time = self.end_time if self.end_time else time.time()
        return current_time - self.start_time + self.elapsed_paused_time

    def get_remaining_time(self) -> float:
        """
        Get remaining time in seconds (for countdown mode)
        
        Returns:
            float: Remaining time in seconds
        """
        elapsed = self.get_elapsed_time()
        remaining = max(0, self.duration - elapsed)
        
        # Auto-stop when countdown reaches zero
        if remaining == 0 and self.is_running:
            self.stop()
            
        return remaining

    def is_time_up(self) -> bool:
        """
        Check if timer duration has been reached
        
        Returns:
            bool: True if time is up
        """
        return self.get_elapsed_time() >= self.duration

    def get_formatted_time(self, elapsed: bool = True) -> str:
        """
        Get formatted time string (MM:SS)
        
        Args:
            elapsed: If True, return elapsed time; if False, return remaining time
            
        Returns:
            str: Formatted time string
        """
        time_seconds = self.get_elapsed_time() if elapsed else self.get_remaining_time()
        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def set_callback(self, callback: Callable[[float], None]) -> None:
        """
        Set callback function for real-time updates
        
        Args:
            callback: Function to call with elapsed time
        """
        self.callback = callback

    def _timer_loop(self) -> None:
        """Background thread loop for real-time updates"""
        while not self._stop_event.is_set() and self.is_running:
            if not self.is_paused and self.callback:
                try:
                    elapsed = self.get_elapsed_time()
                    self.callback(elapsed)
                except Exception as e:
                    print(f"Timer callback error: {e}")
                    
            # Update every 100ms for smooth real-time updates
            time.sleep(0.1)

# Example usage and testing
if __name__ == "__main__":
    def on_time_update(elapsed_time):
        print(f"Elapsed: {elapsed_time:.1f}s")
    
    # Test basic functionality
    timer = Timer(duration=5, callback=on_time_update)
    
    print("Starting 5-second timer...")
    timer.start()
    
    # Let it run for a bit
    time.sleep(6)
    
    print(f"Final elapsed time: {timer.get_elapsed_time():.1f}s")
    print(f"Formatted time: {timer.get_formatted_time()}")
    print(f"Time up: {timer.is_time_up()}")