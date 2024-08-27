from typing import List

from sqlalchemy import Insert, Select, Update, Delete

from src.model.word import Word
from src.dto.word import WordCreate, WordUpdate
from src.repository.base_repo import BaseRepository

from src.model.category import Category


class WordRepository(BaseRepository):
    async def create_word(self, category_id: int, word_create: WordCreate) -> Word:
        async with self.db_session() as db_session:
            word = Word(main_language=word_create.main_language, second_language=word_create.second_language,
                                       transcription=word_create.transcription, category_id=category_id)

            db_session.add(word)
            await db_session.commit()
            await db_session.refresh(word)

            return word

    async def get_word_by_id(self, word_id: int) -> Word:
        async with self.db_session() as db_session:
            stmt = Select(Word).where(Word.id == word_id)

            result = await db_session.execute(statement=stmt)
            word = result.scalar()

            return word

    async def get_words_by_category_id(self, category_id: int) -> List[Word]:
        async with self.db_session() as db_session:
            stmt = Select(Word).where(Word.category_id == category_id)

            words_list = await db_session.execute(statement=stmt)

            words_list = [
                element
                for element
                in words_list.scalars()
            ]

            return words_list

    async def update_word(self, word: Word, word_update: WordUpdate) -> Word:
        async with self.db_session() as db_session:
            db_session.add(word)

            if word_update.main_language:
                word.main_language = word_update.main_language

            if word_update.second_language:
                word.second_language = word_update.second_language

            if word_update.transcription:
                word.transcription = word_update.transcription

            await db_session.commit()
            await db_session.refresh(word)

            return word

    async def delete_word(self, word_id: int) -> int | None:
        async with self.db_session() as db_session:
            stmt = Delete(Word).where(Word.id == word_id)

            await db_session.execute(statement=stmt)
            await db_session.commit()

            return word_id
