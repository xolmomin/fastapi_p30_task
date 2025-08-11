from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class ResponseSchema(BaseModel, Generic[T]):
    message: str
    data: T | None = None


class CreateCategory(BaseModel):
    name: str


class UpdateCategory(BaseModel):
    name: str | None = None

    class Config:
        from_attributes = True


class ReadCategory(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
