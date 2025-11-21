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
    
    
    def get_text_by_difficulty(self, difficulty: str) -> str:
        """
        Get random text by specific difficulty level
        
        Args:
            difficulty: Difficulty level (easy, medium, hard, programming)
            
        Returns:
            str: Random text of specified difficulty
        """
        if difficulty not in self.default_texts:
            difficulty = "medium"
            
        texts = self.default_texts[difficulty]
        text = random.choice(texts)
        self.current_text = text
        return self._format_text(text)
    
    
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
    
    def load_texts_from_file(self, file_path: str) -> bool:
        """
        Load texts from a file, one text per line
        
        Args:
            file_path: Path to the text file
        Returns:
            bool: True if texts were loaded successfully
        """

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.read()

            texts = self._split_text_into_segments(lines)

            for text in texts:
                self.add_costum_text(text)

            return len(texts) > 0

        except Exception as e:
            print(f"Error loading texts from file: {e}")
            return False
    
    def _split_text_into_segments(self, content: str) -> List[str]:
        """Split large text into smaller segments based on punctuation
        
        Args:
            content: Large block of text
            
        Returns:
            List[str]: List of text segments
        """
        # Split by sentence-ending punctuation followed by space/newline
        sentences = re.split(r'(?<=[.!?])\s+', content)
        segments = []
        
        current_segment = ""
        max_length = 200  # Max length for each segment

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if current_segment and len(current_segment+" "+sentence) > max_length:
                segments.append(self._formated_text(current_segment))
                current_segment = sentence
            else:
                current_segment += " " + sentence if current_segment else sentence

        if current_segment:
            segments.append(self._formated_text(current_segment))

        return segments
    
    def get_text_statistics(self, text: str = None) -> dict:
        """
        Get statistics of the given text or current text
        
        Args:
            text: Optional text to analyze. If None, uses current_text.
        
        Returns:
            dict: Statistics including character count and word count
        """
        if text is None:
            text = self.current_text

        if not text:
            return {}
        
        # Calculate word count(including spaces)
        words = text.split()
        total_characters = len(words)

        # Calculate character count (excluding spaces)
        chars_no_spaces = len(text.replace(" ", ""))

        # Calculate word count (including spaces)
        word_count = len(text.split())

        # count sentences
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])

        # Average word length
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0

        # Estimated difificulty level based on average word length
        if avg_word_length < 4:
            estimated_difficulty = "easy"
        elif avg_word_length < 6:
            estimated_difficulty = "medium"
        else:
            estimated_difficulty = "hard"

        return {"total_characters": total_characters, "chars_no_spaces": chars_no_spaces, "word_count": word_count, "sentence_count": sentence_count, "avg_word_length": avg_word_length, "estimated_difficulty": estimated_difficulty}

    def get_all_texts(self) -> dict:
        """
        Get all available texts organized by source
        
        Returns:
            dict: All texts organized by source and difficulty
        """
        return {
            "default": self.default_texts,
            "custom": self.custom_texts
        }

    def clear_custom_texts(self) -> None:
        """Clear all custom texts"""
        self.custom_texts.clear()

    def get_text_count(self) -> dict:
        """
        Get count of texts by category
        
        Returns:
            dict: Text counts by category
        """
        counts = {"custom": len(self.custom_texts)}
        
        for difficulty, texts in self.default_texts.items():
            counts[difficulty] = len(texts)
            
        return counts
    
if __name__ == "__main__":
    # texts = [
    #     "The quick brown fox jumps over the lazy dog.",
    #     "Pack my box with five dozen liquor jugs.",
    #     "How vexingly quick daft zebras jump!"
    # ]
    
    # manager = TextManager(texts)
    # random_text = manager.get_random_text()
    # print("Random Text:", random_text)
    
    # user_input = input("Type the above text: ")
    # correct, total = manager.compare_texts(user_input)
    # print(f"Correct Characters: {correct} out of {total}")

    print(dir(TextManager))