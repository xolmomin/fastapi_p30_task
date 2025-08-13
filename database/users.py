from sqlalchemy import Integer, String, Float, Enum, select
from sqlalchemy.orm import Mapped, mapped_column

from database import Model
from database.base_model import db


class User(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    @classmethod
    async def get_by_username(cls, username: str):
        query = select(cls).where(cls.username == username)
        return (await db.execute(query)).scalar()
