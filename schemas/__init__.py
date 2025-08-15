from typing import TypeVar, Generic

from pydantic import BaseModel

from schemas.auth import RegisterForm
from schemas.categories import CreateCategory, ReadCategory, UpdateCategory
from schemas.products import CreateProduct

T = TypeVar('T', bound=BaseModel)


class ResponseSchema(BaseModel, Generic[T]):
    message: str
    data: T | None = None


__all__ = [
    'ResponseSchema',
    'CreateCategory',
    'ReadCategory',
    'CreateProduct',
    'UpdateCategory',
    'RegisterForm',
]