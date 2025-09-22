from src.database.expenses_repo import Expenses
from src.database.users_repo import Users
from src.services.expense_service import ExpenseService
from src.services.user_service import UserService


def get_user_service():
    return UserService(Users())

def get_expense_service():
    return ExpenseService(expenses=Expenses(), users=Users())
