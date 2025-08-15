from typing import Self

from pydantic import BaseModel, Field, EmailStr, field_validator, validator, model_validator
from pydantic_core import ValidationError
from pydantic_core.core_schema import ValidationInfo

from utils.security import get_password_hash


class RegisterForm(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=255, examples=['botir'])
    username: str = Field(..., min_length=1, examples=['botir'])
    email: EmailStr = Field(..., min_length=1, examples=['test@gmail.com'])
    password: str = Field(..., min_length=1, examples=['1'])
    confirm_password: str = Field(..., min_length=1, examples=['1'])

    # @field_validator('password')
    # def password_validator(cls, value):
    #     if len(value) < 8:
    #         raise ValueError('Password must be at least 8 characters')
    #     return value

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')

        self.password = get_password_hash(self.password)
        return self.model_dump(exclude={'confirm_password'})


class LoginPhoneForm(BaseModel):
    phone_number: str = Field(..., title='1', min_length=9, examples=['998935248052'])

    @field_validator('phone_number')
    def phone_number_validator(cls, value: str):
        if not value.startswith('998'):
            raise ValueError('Uzbek nomeri bolsin')
        return value.removeprefix('+')
