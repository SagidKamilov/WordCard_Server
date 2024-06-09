from typing import List

from sqlalchemy import Insert, Select, Update, Delete

from src.model.word import Word
from src.dto.word import WordCreate, WordUpdate
from src.repository.base_repo import BaseRepository

from src.model.category import Category


class WordRepository(BaseRepository):
    async def create_word(self, category_id: int, word_create: WordCreate) -> Word:
        stmt = Insert(Word).values(main_language=word_create.main_language, second_language=word_create.second_language,
                                   transcription=word_create.transcription, category_id=category_id)

        result = await self.db_session.execute(statement=stmt)
        word = result.scalar()

        return word

    async def get_word_by_id(self, word_id: int) -> Word | None:
        stmt = Select(Word).where(Word.id == word_id)

        result = await self.db_session.execute(statement=stmt)
        word = result.scalar()

        if not word:
            return None

        return word

    async def get_words_by_category_id(self, category_id: int) -> List[Word] | None:
        stmt = Select(Word).where(Category.id == category_id)

        words_list = await self.db_session.execute(statement=stmt)
        if not words_list:
            return None

        words_list = [
            element.scalar()
            for element
            in words_list
        ]

        return words_list

    async def update_word(self, word_id: int, word_update: WordUpdate) -> Word | None:
        word = await self.get_word_by_id(word_id=word_id)

        if not word:
            return None

        if word_update.main_language:
            word.main_language = word_update.main_language

        if word_update.second_language:
            word.second_language = word_update.second_language

        if word_update.transcription:
            word.transcription = word_update.transcription

        await self.db_session.commit()

        return word

    async def delete_word(self, word_id: int) -> int | None:
        stmt = Delete(Word).where(Word.id == word_id)

        await self.db_session.execute(statement=stmt)
        await self.db_session.commit()

        return word_id
