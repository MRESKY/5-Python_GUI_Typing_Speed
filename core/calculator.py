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

# Handle imports for both standalone and module execution
try:
    from .contracts.i_calculator import iCalculator
except ImportError:
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from contracts.i_calculator import iCalculator

class Calculator(iCalculator):
    
    @staticmethod
    def calculate_wpm(correct_chars: int, total_chars: int, time_minutes: float) -> Tuple[float, float, float]:
        """
        Calculate WPM, accuracy, and return time taken
        
        Args:
            correct_chars: Number of correctly typed characters
            total_chars: Total number of characters in the target text
            time_minutes: Time taken in minutes
            
        Returns:
            tuple: (wpm, accuracy_percentage, time_minutes)
        """
        if time_minutes <= 0:
            return 0.0, 0.0, time_minutes
            
        # Standard WPM calculation: correct characters / 5 / time in minutes
        # The "5" represents average characters per word
        wpm = (correct_chars / 5) / time_minutes
        
        # Accuracy: correct characters / total characters * 100
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0.0
        
        return round(wpm, 2), round(accuracy, 2), time_minutes

    @staticmethod
    def calculate_real_time_wpm(correct_chars: int, time_seconds: float) -> float:
        """
        Calculate real-time WPM for live updates
        
        Args:
            correct_chars: Number of correctly typed characters so far
            time_seconds: Time elapsed in seconds
            
        Returns:
            float: Current WPM
        """
        if time_seconds <= 0:
            return 0.0
            
        # Convert seconds to minutes and calculate WPM
        time_minutes = time_seconds / 60.0
        wpm = (correct_chars / 5) / time_minutes
        
        return round(wpm, 1)

    @staticmethod
    def calculate_detailed_accuracy(user_input: str, target_text: str) -> Dict[str, float]:
        """
        Calculate detailed accuracy metrics
        
        Args:
            user_input: What the user typed
            target_text: What they should have typed
            
        Returns:
            dict: Detailed accuracy metrics
        """
        if not target_text:
            return {"accuracy": 0.0, "errors": 0, "correct_chars": 0}
            
        min_length = min(len(user_input), len(target_text))
        correct_chars = 0
        errors = 0
        
        # Character-by-character comparison
        for i in range(min_length):
            if user_input[i] == target_text[i]:
                correct_chars += 1
            else:
                errors += 1
                
        # Account for missing characters (if user input is shorter)
        if len(user_input) < len(target_text):
            errors += len(target_text) - len(user_input)
            
        # Account for extra characters (if user input is longer)
        if len(user_input) > len(target_text):
            errors += len(user_input) - len(target_text)
            
        total_chars = len(target_text)
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0.0
        error_rate = (errors / total_chars) * 100 if total_chars > 0 else 0.0
        
        return {
            "accuracy": round(accuracy, 2),
            "correct_chars": correct_chars,
            "total_chars": total_chars,
            "errors": errors,
            "error_rate": round(error_rate, 2),
            "completion": round((min_length / total_chars) * 100, 2) if total_chars > 0 else 0.0
        }

    @staticmethod
    def calculate_words_per_minute_net(correct_chars: int, errors: int, time_minutes: float) -> float:
        """
        Calculate Net WPM (accounting for errors)
        
        Args:
            correct_chars: Number of correctly typed characters
            errors: Number of errors made
            time_minutes: Time taken in minutes
            
        Returns:
            float: Net WPM (WPM minus error penalty)
        """
        if time_minutes <= 0:
            return 0.0
            
        # Gross WPM
        gross_wpm = (correct_chars / 5) / time_minutes
        
        # Error penalty (subtract 1 WPM per error)
        error_penalty = errors / time_minutes
        
        # Net WPM cannot be negative
        net_wpm = max(0, gross_wpm - error_penalty)
        
        return round(net_wpm, 2)

    @staticmethod
    def calculate_typing_speed_grade(wpm: float, accuracy: float) -> Dict[str, str]:
        """
        Calculate typing speed grade and performance level
        
        Args:
            wpm: Words per minute
            accuracy: Accuracy percentage
            
        Returns:
            dict: Grade and performance information
        """
        # Determine speed grade
        if wpm >= 80:
            speed_grade = "Expert"
        elif wpm >= 60:
            speed_grade = "Advanced"
        elif wpm >= 40:
            speed_grade = "Intermediate"
        elif wpm >= 25:
            speed_grade = "Beginner"
        else:
            speed_grade = "Novice"
            
        # Determine accuracy grade
        if accuracy >= 98:
            accuracy_grade = "Excellent"
        elif accuracy >= 95:
            accuracy_grade = "Very Good"
        elif accuracy >= 90:
            accuracy_grade = "Good"
        elif accuracy >= 80:
            accuracy_grade = "Fair"
        else:
            accuracy_grade = "Poor"
            
        # Overall performance
        if wpm >= 60 and accuracy >= 95:
            overall = "Professional"
        elif wpm >= 40 and accuracy >= 90:
            overall = "Proficient"
        elif wpm >= 25 and accuracy >= 80:
            overall = "Developing"
        else:
            overall = "Learning"
            
        return {
            "speed_grade": speed_grade,
            "accuracy_grade": accuracy_grade,
            "overall_performance": overall
        }

    @staticmethod
    def calculate_progress_metrics(session_data: List[Dict]) -> Dict[str, float]:
        """
        Calculate progress metrics from multiple typing sessions
        
        Args:
            session_data: List of session dictionaries with wpm, accuracy, etc.
            
        Returns:
            dict: Progress metrics and trends
        """
        if not session_data:
            return {}
            
        wpm_values = [session.get('wpm', 0) for session in session_data]
        accuracy_values = [session.get('accuracy', 0) for session in session_data]
        
        # Calculate averages
        avg_wpm = sum(wpm_values) / len(wpm_values)
        avg_accuracy = sum(accuracy_values) / len(accuracy_values)
        
        # Calculate improvement trends (compare first half vs second half)
        mid_point = len(session_data) // 2
        if mid_point > 0:
            first_half_wpm = sum(wpm_values[:mid_point]) / mid_point
            second_half_wpm = sum(wpm_values[mid_point:]) / (len(wpm_values) - mid_point)
            wpm_improvement = ((second_half_wpm - first_half_wpm) / first_half_wpm) * 100 if first_half_wpm > 0 else 0
            
            first_half_accuracy = sum(accuracy_values[:mid_point]) / mid_point
            second_half_accuracy = sum(accuracy_values[mid_point:]) / (len(accuracy_values) - mid_point)
            accuracy_improvement = second_half_accuracy - first_half_accuracy
        else:
            wpm_improvement = 0
            accuracy_improvement = 0
            
        # Best and worst performances
        best_wpm = max(wpm_values)
        worst_wpm = min(wpm_values)
        best_accuracy = max(accuracy_values)
        worst_accuracy = min(accuracy_values)
        
        return {
            "total_sessions": len(session_data),
            "average_wpm": round(avg_wpm, 2),
            "average_accuracy": round(avg_accuracy, 2),
            "best_wpm": round(best_wpm, 2),
            "worst_wpm": round(worst_wpm, 2),
            "best_accuracy": round(best_accuracy, 2),
            "worst_accuracy": round(worst_accuracy, 2),
            "wpm_improvement_percent": round(wpm_improvement, 2),
            "accuracy_improvement_percent": round(accuracy_improvement, 2)
        }

    @staticmethod
    def estimate_completion_time(current_position: int, total_chars: int, current_wpm: float) -> float:
        """
        Estimate time to complete typing based on current performance
        
        Args:
            current_position: Current character position
            total_chars: Total characters to type
            current_wpm: Current WPM
            
        Returns:
            float: Estimated completion time in seconds
        """
        if current_wpm <= 0 or current_position >= total_chars:
            return 0.0
            
        remaining_chars = total_chars - current_position
        chars_per_second = (current_wpm * 5) / 60  # Convert WPM to chars per second
        
        estimated_seconds = remaining_chars / chars_per_second if chars_per_second > 0 else 0
        
        return round(estimated_seconds, 1)

# Example usage and testing
if __name__ == "__main__":
    # Test basic WPM calculation
    correct_chars = 250
    total_chars = 300
    time_minutes = 2.0

    wpm, accuracy, time_taken = Calculator.calculate_wpm(correct_chars, total_chars, time_minutes)
    print(f"WPM: {wpm}, Accuracy: {accuracy}%, Time: {time_taken} minutes")

    # Test real-time WPM
    real_time_wpm = Calculator.calculate_real_time_wpm(150, 120)  # 150 chars in 2 minutes
    print(f"Real-time WPM: {real_time_wpm}")

    # Test detailed accuracy
    user_text = "The quick brown fox jumps"
    target_text = "The quick brown fox jumps over the lazy dog"
    accuracy_details = Calculator.calculate_detailed_accuracy(user_text, target_text)
    print(f"Detailed accuracy: {accuracy_details}")

    # Test performance grading
    grade_info = Calculator.calculate_typing_speed_grade(45, 92)
    print(f"Performance grade: {grade_info}")
    
    # Test progress metrics
    sessions = [
        {"wpm": 30, "accuracy": 85},
        {"wpm": 35, "accuracy": 88},
        {"wpm": 40, "accuracy": 90},
        {"wpm": 42, "accuracy": 92}
    ]
    progress = Calculator.calculate_progress_metrics(sessions)
    print(f"Progress metrics: {progress}")