import typer
from rich.console import Console

from property_tracker.database import session
from property_tracker.repositories import InvestorRepository
from property_tracker.services import InvestorService

app = typer.Typer()
console = Console()


@app.command()
def add(name, contact, portfolio_value):
    """
    Add a new investor

    Args:
        name (str): Name of the investor
        contact (str): Contact information of the investor
        portfolio_value (float): Value of the investor's portfolio
    """
    investor_repository = InvestorRepository(session)
    investor_service = InvestorService(investor_repository)
    investor = investor_service.create_investor(name, contact, portfolio_value)
    session.close()
    typer.echo(f"Investor {investor.name} added successfully")


# Additional commands for Property, Tenant, Lease, MaintenanceRequest, Payment, Expense, TaxPayment would be similar
