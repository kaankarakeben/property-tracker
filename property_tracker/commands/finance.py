import typer
from rich.console import Console
from rich.table import Table

from property_tracker.database import session
from property_tracker.repositories import FinanceRepository

app = typer.Typer()
console = Console()


@app.command()
def ls(entity: str):
    """
    List all instances of an entity.
    """

    if entity == "mortgages":
        finance_repository = FinanceRepository(session)
        mortgages = finance_repository.get_all_mortgages()
        table = Table(title="Mortgages")
        table.add_column("ID")
        table.add_column("Property ID")
        table.add_column("Investor ID")
        table.add_column("Start Date")
        table.add_column("End Date")
        table.add_column("Principal")
        table.add_column("Payment Term")
        table.add_column("Annual Interest Rate")

        for mortgage in mortgages:
            table.add_row(
                str(mortgage.id),
                str(mortgage.property_id),
                str(mortgage.investor_id),
                str(mortgage.start_date),
                str(mortgage.end_date),
                str(mortgage.principal),
                str(mortgage.payment_term),
                str(mortgage.annual_interest_rate),
            )
        console.print(table)

    if entity == "expenses":
        finance_repository = FinanceRepository(session)
        expenses = finance_repository.get_all_expenses()
        table = Table(title="Expenses")
        table.add_column("ID")
        table.add_column("Description")
        table.add_column("Amount")
        table.add_column("Date")
        table.add_column("Investor ID")
        table.add_column("Property ID")
        for expense in expenses:
            table.add_row(
                str(expense.id),
                expense.description,
                str(expense.amount),
                str(expense.date),
                str(expense.investor_id),
                str(expense.property_id),
            )
        console.print(table)
