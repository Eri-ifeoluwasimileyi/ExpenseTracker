from abc import ABC, abstractmethod

from src.schemas.user_schemas import CreateUser, UpdateUser


class UserInterface(ABC):

    @abstractmethod
    def add_user(self, user: CreateUser) -> dict:
        pass

    @abstractmethod
    def update_user(self, user: UpdateUser):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str):
        pass

    @abstractmethod
    def get_user_by_email(self, email: str):
        pass

    @abstractmethod
    def update_balance(self, user_id: str, new_balance: float):
        pass

    @abstractmethod
    def user_blacklist_token(self, token: str):
        pass

    @abstractmethod
    def check_blacklisted_token(self, token: str):
        pass
