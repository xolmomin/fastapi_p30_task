from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Model


class Product(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
