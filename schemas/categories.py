from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str


class ReadCategory(BaseModel):
    id: int
    name: str
