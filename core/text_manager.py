import random
from .contracts.i_text_manager import TextManager as ITextManager


class TextManager(ITextManager):
    def __init__(self, texts=None):
        if texts is None:
            texts = []
            raise ValueError("TextManager requires a list of texts.")
        self.texts = texts
        self.current_text = None

    def get_random_text(self):
        if not self.texts:
            return None
        self.current_text = random.choice(self.texts)
        return self.current_text
    
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