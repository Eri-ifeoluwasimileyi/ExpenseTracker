from flask import abort

from exceptions.user_exceptions import UserNotFoundError, InvalidAmountError, UserAlreadyExistsError, \
    IncorrectPasswordError
from src.database.user_interface import UserInterface
from src.schemas.user_schemas import CreateUser, UpdateUser, LoginUser
from src.utils.password import hash_password, verify_password


class UserService:
    def __init__(self, users: UserInterface):
        self.users = users

    def register_user(self, user: CreateUser):
        self.__check_email(user.email)

        user.password = hash_password(user.password)
        return self.users.add_user(user)

    def verify_user(self, user: LoginUser):
        found_user = self.users.get_user_by_email(user.email)
        if found_user is None:
            raise UserNotFoundError('User not found', 404)
        if verify_password(
                plain_password=user.password,
                hashed_password=found_user['password']
        ):
            return found_user
        raise IncorrectPasswordError('Incorrect password', 404)

    def update_user(self, update_user: UpdateUser):
        if update_user.email is not None:
            self.__check_email(update_user.email)

        if update_user.password is not None:
            update_user.password = hash_password(update_user.password)

        return self.users.update_user(update_user)

    def get_user(self, user_id: str):
        user = self.users.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User {user_id} not found", 404)
        return user


    def fund_user_balance(self, user_id: str, amount: float):
        user_data = self.users.get_user_by_id(user_id)
        if not user_data:
            raise UserNotFoundError("User not found", 404)

        if amount <= 0:
            raise InvalidAmountError("Funding amount must be greater than zero", 404)

        new_balance = user_data["initial_balance"] + amount
        self.users.update_balance(user_id=user_id, new_balance=new_balance)

        return {
            "message": "Wallet funded successfully",
            "new_balance": new_balance
        }



    def __check_email(self, email: str):
        if self.users.get_user_by_email(email) is not None:
            raise UserAlreadyExistsError(f"User {email} already exists", 400)

    def blacklist_token(self, token: str):
        self.users.user_blacklist_token(token)

    def is_jti_blacklisted(self, token: str):
        return self.users.check_blacklisted_token(token)
