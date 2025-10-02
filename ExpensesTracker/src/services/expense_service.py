from exceptions.expense_exceptions import *
from exceptions.user_exceptions import UserNotFoundError
from src.database.expenses_interface import ExpensesInterface
from src.database.user_interface import UserInterface
from src.schemas.expense_schemas import AddExpense, DeleteExpense, UpdateExpense


class ExpenseService:
    def __init__(self, expenses: ExpensesInterface, users: UserInterface):
        self.expenses = expenses
        self.users = users

    def add_expense(self, expense: AddExpense):
        user_data = self.users.get_user_by_id(expense.user_id)

        if user_data is None:
            raise UserNotFoundError("User not found", 404)
        if expense.amount > user_data["balance"]:
            raise NotEnoughBalanceError("You don't have enough money to add this expense", 400)

        self.users.update_balance(
            user_id=expense.user_id,
            new_balance=user_data["balance"] - expense.amount
        )

        return self.expenses.add_expense(expense)

    def get_user_expense(self, expense_id: str):
        expense_data = self.expenses.find_expense(expense_id)
        if expense_data is None:
            raise ExpenseNotFoundError("Expense not found", 404)
        return expense_data

    def get_users_expenses(self, user_id: str):
        expenses = self.expenses.get_expenses(user_id)
        if not expenses:
            raise ExpenseNotFoundError("No expenses found", 404)
        return expenses

    def update_user_expense(self, expense_id: str, update_data: UpdateExpense):
        expense = self.expenses.find_expense(expense_id)
        if expense is None:
            raise ExpenseNotFoundError("Expense not found", 404)

        updates = update_data.model_dump(exclude_none=True)
        if not updates:
            raise NoUpdatesFoundError("No updates found", 404)

        #if amount is updated, it should adjust the balance
        if 'amount' in updates:
            user_data = self.users.get_user_by_id(expense['user_id'])
            if user_data is None:
                raise UserNotFoundError("User not found", 404)

            old_amount = expense['amount']
            new_amount = updates['amount']
            diff = old_amount - new_amount

            new_balance = user_data["balance"] + diff
            if new_balance < 0:
                raise NotEnoughBalanceError("You don't have enough money to add this expense", 400)

            self.users.update_balance(
                user_id=expense['user_id'],
                new_balance=new_balance
            )

        return self.expenses.update_expense(expense_id, updates)

    def delete_user_expenses(self, delete: DeleteExpense):
        user_data = self.users.get_user_by_id(delete.user_id)
        expense_data = self.expenses.find_expense(delete.expense_id)
        if expense_data is None or user_data is None:
            raise NoInfoFoundError("No Info found", 404)

        self.users.update_balance(
            user_id=delete.user_id,
            new_balance=user_data["balance"] + expense_data["amount"]
        )

        return self.expenses.delete_expense(delete.expense_id)

    def calculate_total_expenses(self, user_id: str):
        expenses = self.expenses.get_expenses(user_id)
        if not expenses:
            return 0
        return sum([expense["amount"] for expense in expenses], 0)
