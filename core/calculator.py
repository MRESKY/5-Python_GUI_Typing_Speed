"""
Complete Calculator Implementation with Advenced Features
==========================================================

This module provides a Calculator class that supports basic arithmetic operations
- Real-time WPM calculation
- Accuracy tracking
- Error rate
- Performance statistics
"""

from typing import Tuple, Dict, List
from contracts.i_calculator import iCalculator

class Calculator(iCalculator):

    @staticmethod
    def calculate_wpm(correct_chars: int, total_chars: int, time_minutes: float) -> tuple[float, float, float]:
        """
        Calculate WPM, accuracy, and return time taken

        Args:
            correct_chars (int): Number of correctly typed characters
            total_chars (int): Total number of characters typed
            time_minutes (float): Time taken in minutes

        Returns:
            tuple: (WPM, accuracy percentage, time taken in minutes)
        """
        if time_minutes <= 0:
            return 0.0, 0.0, time_minutes
        
        wpm = (correct_chars / 5) / time_minutes
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0.0

        return round(wpm, 2), round(accuracy, 2), time_minutes