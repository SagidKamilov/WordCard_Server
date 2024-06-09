from typing import List

from src.repository.word import WordRepository
from src.model.word import Word
from src.dto.word import WordCreate, WordUpdate, WordResponse


class WordService:
    def __init__(self, word_repo: WordRepository):
        self.word_repo = word_repo

    async def create_word(self, category_id: int, word_create: WordCreate) -> WordResponse:
        word = await self.word_repo.create_word(category_id=category_id, word_create=word_create)

        return WordResponse(
            id=word.id,
            main_language=word.main_language,
            second_language=word.second_language,
            transcription=word.transcription
        )

    async def get_word(self, word_id: int) -> WordResponse:
        word = await self.word_repo.get_word_by_id(word_id=word_id)

        if not word:
            raise Exception(f"Слово с id = `{word_id}` не найдено!")

        return WordResponse(
            id=word.id,
            main_language=word.main_language,
            second_language=word.second_language,
            transcription=word.transcription
        )

    async def get_words(self, category_id: int) -> List[WordResponse]:
        words = await self.word_repo.get_words_by_category_id(category_id=category_id)

        response_words = [
            WordResponse(
                id=element.id,
                main_language=element.main_language,
                second_language=element.second_language,
                transcription=element.transcription
            )
            for element
            in words
        ]

        return response_words

    async def update_word(self, word_id: int, word_update: WordUpdate) -> WordResponse:
        check_exist = await self.check_word_exist(word_id=word_id)

        if not check_exist:
            raise Exception(f"Слово с id = `{word_id}` не было найдено!")

        word = await self.word_repo.update_word(word_id=word_id, word_update=word_update)

        return WordResponse(
            id=word.id,
            main_language=word.main_language,
            second_language=word.second_language,
            transcription=word.transcription
        )

    async def delete_word(self, word_id: int) -> int:
        check_user_exist: bool = await self.check_word_exist(word_id=word_id)

        if not check_user_exist:
            raise Exception(f"Слово с id = `{word_id}` не было найдено!")

        result: int = await self.word_repo.delete_word(word_id=word_id)

        return result

    async def check_word_exist(self, word_id: int) -> bool:
        word = await self.word_repo.get_word_by_id(word_id=word_id)

        if word:
            return True
        else:
            return False
