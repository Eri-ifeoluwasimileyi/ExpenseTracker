from abc import ABC, abstractmethod

from src.schemas.expense_schemas import DeleteExpense, AddExpense, UpdateExpense


class ExpensesInterface(ABC):
    @abstractmethod
    def add_expense(self, expense: AddExpense):
        pass

    @abstractmethod
    def find_expense(self, expense_id: str):
        pass

    @abstractmethod
    def get_expenses(self, user_id: str):
        pass

    @abstractmethod
    def update_expense(self, expense_id: str, updates):
        pass

    @abstractmethod
    def delete_expense(self, expense_id: str):
        pass