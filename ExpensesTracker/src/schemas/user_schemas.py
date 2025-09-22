from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from src.utils.validators import name_pattern


class CreateUser(BaseModel):
    first_name: str = Field(..., pattern=name_pattern)
    last_name: str = Field(..., pattern=name_pattern)
    email: EmailStr = Field(..., min_length=10)
    password: str = Field(..., min_length=8)
    initial_balance: float = 0

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    id: str
    first_name: Optional[str] = Field(default=None, pattern=name_pattern)
    last_name: Optional[str] = Field(default=None, pattern=name_pattern)
    email: Optional[str] = Field(default=None, min_length=10)
    password: Optional[str] = Field(default=None, min_length=8)
    initial_balance: Optional[float] = Field(default=None, gt=0)

