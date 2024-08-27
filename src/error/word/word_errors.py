from src.error.base_error import CustomError


class WordNotExists(CustomError):
    def __init__(self, word_id: int):
        self.word_id = word_id
        self.message = f"Слово с id = {self.word_id} не существует!"
        super().__init__(self.message)
