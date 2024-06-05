from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base_model import Base


class Word(Base):
    __tablename__ = "word_word_card"

    main_language: Mapped[str] = mapped_column(name="main_language", type_=String(255), nullable=False, unique=False)
    second_language: Mapped[str] = mapped_column(name="second_language", type_=String(255), nullable=False, unique=False)
    transcription: Mapped[str] = mapped_column(name="transcription", type_=String(255), nullable=True, unique=False)

    category_id: Mapped[int] = mapped_column("category_id", ForeignKey("category_word_card.id"))
    category: Mapped["category_word_card"] = relationship("category_word_card", back_populates="words")
