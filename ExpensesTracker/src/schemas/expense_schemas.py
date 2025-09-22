from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.utils.validators import string_pattern


class AddExpense(BaseModel):
    user_id: str
    title: Optional[str] = Field(..., pattern=string_pattern, min_length=2)
    description: str = Field(..., pattern=string_pattern, min_length=2)
    amount: float = Field(..., gt=0)
    date_added:datetime = datetime.now()


class UpdateExpense(BaseModel):
    user_id: str
    title: Optional[str] = Field(None, pattern=string_pattern, min_length=2)
    description: Optional[str] = Field(None, pattern=string_pattern, min_length=2)
    amount: Optional[float] = Field(None, gt=0)

class DeleteExpense(BaseModel):
    user_id: str
    expense_id: str


