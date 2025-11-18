from core.contracts.i_calculator import iCalculator

class Calculator(iCalculator):
    @staticmethod
    def calculate_wpm(correct_chars: int, total_chars: int, time_minutes: float) -> tuple:
        """
        Calculate WPM, accuracy, and return time taken
        
        Args:
            correct_chars: Number of correctly typed characters
            total_chars: Total number of characters in the text
            time_minutes: Time taken in minutes
            
        Returns:
            tuple: (wpm, accuracy_percentage, time_minutes)
        """
        if time_minutes <= 0:
            return 0, 0, time_minutes
            
        # Standard WPM calculation: correct characters / 5 / time in minutes
        wpm = (correct_chars / 5) / time_minutes
        
        # Accuracy: correct characters / total characters * 100
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0
        
        return round(wpm, 2), round(accuracy, 2), time_minutes

if __name__ == "__main__":
    correct_chars = 250
    total_chars = 300  # Total characters in the text, not words * 5
    time_minutes = 2.0

    wpm, accuracy, time_taken = Calculator.calculate_wpm(correct_chars, total_chars, time_minutes)
    print(f"WPM: {wpm}, Accuracy: {accuracy}%, Time Taken: {time_taken} minutes")