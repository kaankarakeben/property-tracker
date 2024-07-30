from property_tracker.models import Expense
from property_tracker.repositories import ExpenseRepository


class ExpenseService:
    """
    Service class for Expense
    """

    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repository = expense_repository

    def create_expense(self, property_id: int, description: str, cost: float):
        """
        Create a new expense
        :param property_id: int
        :param description: str
        :param cost: float
        :return: Expense
        """

        new_expense = Expense(
            property_id=property_id, description=description, cost=cost
        )
        return self.expense_repository.add_expense(new_expense)

    def get_expense(self, expense_id: int):
        """
        Get an expense by id
        :param expense_id: int
        :return: Expense
        """

        return self.expense_repository.get_expense(expense_id)

    def get_all_expenses(self):
        """
        Get all expenses
        :return: List[Expense]
        """

        return self.expense_repository.get_all_expenses()

    def update_expense(self, expense_id: int, description: str, cost: float):
        """
        Update an expense
        :param expense_id: int
        :param description: str
        :param cost: float
        :return: Expense
        """

        expense = self.get_expense(expense_id)
        expense.description = description
        expense.cost = cost
        return self.expense_repository.update_expense(expense)

    def delete_expense(self, expense_id: int):
        """
        Delete an expense
        :param expense_id: int
        :return: None
        """

        expense = self.get_expense(expense_id)
        self.expense_repository.delete_expense(expense)
