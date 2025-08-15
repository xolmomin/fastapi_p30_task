from pydantic import BaseModel, Field


class LoginForm(BaseModel):
    username: str = Field(..., min_length=1, examples=['botir'])
    password: str = Field(..., min_length=1, examples=['123'])
