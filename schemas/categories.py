from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    address: str


class UpdateCategory(BaseModel):
    name: str | None = None
    address: str | None = None


class ReadCategory(BaseModel):
    id: int
    name: str
    address: str
