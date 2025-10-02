from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

from src.utils.validators import name_pattern


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    balance: float = 0

    @field_validator('first_name', 'last_name', mode='after')
    @classmethod
    def validate_name(cls, value):
        if name_pattern.match(value) is None:
            raise ValueError(f'invalid name: {value}')
        return value

    @field_validator('email', mode='after')
    @classmethod
    def validate_email(cls, value):
        if len(value) < 10:
            raise ValueError(f'invalid email: {value}')
        return value

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError(f'invalid password: {value}')
        return value



class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    id: str
    first_name: Optional[str] = Field(default=None, pattern=name_pattern)
    last_name: Optional[str] = Field(default=None, pattern=name_pattern)
    email: Optional[str] = Field(default=None, min_length=10)
    password: Optional[str] = Field(default=None, min_length=8)
    balance: Optional[float] = Field(default=None, gt=0)

