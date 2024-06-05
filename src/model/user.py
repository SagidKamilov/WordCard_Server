from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base_model import Base


class User(Base):
    __tablename__ = "user_word_card"

    name: Mapped[str] = mapped_column(name="name", type_=String(255), unique=False, nullable=True)
    username: Mapped[str] = mapped_column(name="username", type_=String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(name="hashed_password", type_=Text, unique=False, nullable=False)
