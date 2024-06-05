from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base_model import Base


class UserCategoryList(Base):
    __tablename__ = "user_category_list_word_card"

    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("user_word_card.id"))
    category_id: Mapped[int] = mapped_column("category_id", ForeignKey("category_word_card.id"))
