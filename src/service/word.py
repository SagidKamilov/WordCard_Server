from typing import List

from src.repository.word import WordRepository
from src.dto.word import WordCreate, WordUpdate, WordResponse
from src.error.word.word_errors import WordNotExists


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
            raise WordNotExists(word_id=word_id)

        return WordResponse(
            id=word.id,
            main_language=word.main_language,
            second_language=word.second_language,
            transcription=word.transcription
        )

    async def get_words(self, category_id: int) -> List[WordResponse]:
        words = await self.word_repo.get_words_by_category_id(category_id=category_id)

        response_words = list(map(lambda word: WordResponse(id=word.id, main_language=word.main_language, second_language=word.second_language, transcription=word.transcription), words))

        return response_words

    async def update_word(self, word_id: int, word_update: WordUpdate) -> WordResponse:
        word_exists = await self.word_repo.get_word_by_id(word_id=word_id)

        if not word_exists:
            raise WordNotExists(word_id=word_id)

        word = await self.word_repo.update_word(word=word_exists, word_update=word_update)

        return WordResponse(
            id=word.id,
            main_language=word.main_language,
            second_language=word.second_language,
            transcription=word.transcription
        )

    async def delete_word(self, word_id: int) -> int:
        check_user_exist: bool = await self.check_word_exists(word_id=word_id)

        if not check_user_exist:
            raise WordNotExists(word_id=word_id)

        result: int = await self.word_repo.delete_word(word_id=word_id)

        return result

    async def check_word_exists(self, word_id: int) -> bool:
        word = await self.word_repo.get_word_by_id(word_id=word_id)

        return True if word else False
