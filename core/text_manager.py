import random
import re
from typing import List, Optional
from contracts.i_text_manager import iTextManager


class TextManager(iTextManager):
    def __init__(self, texts: Optional[List[str]] = None):
        """
        Initialize TextManager with a list of texts
        
        Args:
            texts: Optional list of texts to manage
        """
        self.costum_texts = texts or []
        self.current_text = ""
        self.default_texts = self._load_default_texts()
        self.difficulty_level = "medium"

    def _load_default_texts(self) -> dict:
        """Load default texts categorized by difficulty levels"""
        return {
            "easy": [
                "The cat sat on the mat.",
                "A quick brown fox jumps.",
                "She sells sea shells by the sea shore.",
                "The sun is bright today.",
                "Birds fly high in the sky."
            ],
            "medium": [
                "The quick brown fox jumps over the lazy dog.",
                "Pack my box with five dozen liquor jugs.",
                "How vexingly quick daft zebras jump!",
                "Programming is the art of telling another human what one wants the computer to do.",
                "The five boxing wizards jump quickly through the mystical fog."
            ],
            "hard": [
                "Amazingly few discotheques provide jukeboxes with quality music for synchronized dancing.",
                "The job requires extra pluck and zeal from every young wage earner who expects to qualify.",
                "We promptly judged antique ivory buckles for the next prize competition.",
                "Complex algorithms require careful optimization to achieve maximum performance efficiency.",
                "Sophisticated software architecture demands thoughtful consideration of scalability and maintainability."
            ],
            "programming": [
                "def calculate_factorial(n): return 1 if n <= 1 else n * calculate_factorial(n - 1)",
                "class Rectangle: def __init__(self, width, height): self.width = width; self.height = height",
                "import json; data = {'name': 'John', 'age': 30}; json_string = json.dumps(data, indent=2)",
                "try: result = divide(a, b) except ZeroDivisionError: print('Cannot divide by zero')",
                "for i in range(10): if i % 2 == 0: print(f'Even: {i}') else: print(f'Odd: {i}')"
            ]
        }
    
    def get_random_text(self) -> str:
        """
        Get a random text for typing practice
        
        Returns:
            str: Randomly selected text
        """
        if self.costum_texts:
            text = random.choice(self.costum_texts)
        else:
            texts = self.default_texts.get(self.difficulty_level, [])
            text = random.choice(texts) if texts else ""

        self.current_text = text
        return text
    
    
    def set_difficulty_level(self, difficulty: str) -> None:
        """
        Set the difficulty level for text selection

        Args:
            difficulty: Difficulty level (easy, medium, hard, programming)
        """
        if difficulty in self.default_texts:
            self.difficulty_level = difficulty
        else:
            raise ValueError(f"Invalid difficulty level: {difficulty}")
    
    def get_difificulty_level(self) -> str:
        """
        Get the current difficulty level

        Returns:
            str: Current difficulty level
        """
        return self.difficulty_level
    
    def get_available_difficulty_levels(self) -> List[str]:
        """
        Get the list of available difficulty levels

        Returns:
            List[str]: Available difficulty levels
        """
        return list(self.default_texts.keys())
    
    def add_costum_text(self, text: str) -> bool:
        """
        Add costum text to the collection
        
        Args:
            text: Text to add
        
        Returns:
            bool: True if text was added successfully
        """

        if not text or not text.strip():
            return False
        
        formatted_text = self._formated_text(text)
        if formatted_text not in self.costum_texts:
            self.costum_texts.append(formatted_text)
            return True
        
        return False
    
    def _formated_text(self, text: str) -> str:
        """Format text by stripping extra spaces and normalizing whitespace
        
        Args:
            text: Raw text to format
            
        Returns:
            str: Formatted text
        """
        if not text:
            return ""
        
        # Remove leading/trailing whitespace and normalize internal spaces
        text = re.sub(r'\s+', ' ', text.strip())

        if text and text[-1] not in {'.', '!', '?'}:
            text += '.'
        
        return text

    def compare_texts(self, user_input):
        correct_characters = 0
        for x, y in zip(user_input.lower(), self.current_text.lower()):
            if x == y:
                correct_characters += 1
        return correct_characters, len(user_input)

if __name__ == "__main__":
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Pack my box with five dozen liquor jugs.",
        "How vexingly quick daft zebras jump!"
    ]
    
    manager = TextManager(texts)
    random_text = manager.get_random_text()
    print("Random Text:", random_text)
    
    user_input = input("Type the above text: ")
    correct, total = manager.compare_texts(user_input)
    print(f"Correct Characters: {correct} out of {total}")