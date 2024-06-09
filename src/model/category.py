from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base_model import Base


class Category(Base):
    __tablename__ = "category_word_card"

    category_name: Mapped[str] = mapped_column(name="category_name", type_=String, nullable=False, unique=False)

    owner_id: Mapped[int] = mapped_column("owner_id", ForeignKey("user_word_card.id", ondelete="CASCADE"))
