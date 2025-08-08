from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Model


class Category(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
