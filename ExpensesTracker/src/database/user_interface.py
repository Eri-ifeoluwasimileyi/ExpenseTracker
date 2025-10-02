from abc import ABC, abstractmethod
from typing import Optional

from src.schemas.user_schemas import CreateUser, UpdateUser


class UserInterface(ABC):

    @abstractmethod
    def add_user(self, user: CreateUser) -> dict:
        pass

    @abstractmethod
    def update_user(self, user: UpdateUser) -> dict:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[dict]:
        pass

    @abstractmethod
    def update_balance(self, user_id: str, new_balance: float) -> bool:
        pass

    @abstractmethod
    def user_blacklist_token(self, token: str) -> None:
        pass

    @abstractmethod
    def check_blacklisted_token(self, token: str) -> bool:
        pass
