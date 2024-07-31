import typer
from rich.console import Console
from rich.table import Table

from property_tracker.database import session
from property_tracker.repositories import InvestorRepository
from property_tracker.services import InvestorService

app = typer.Typer()
console = Console()


@app.command()
def add(name: str, email: str, phone_number: str, address: str):
    """
    Add a new investor

    Args:
        name (str): Name of the investor
        email (str): Email of the investor
        phone_number (str): Phone number of the investor
        address (str): Address of the investor
    """
    investor_repository = InvestorRepository(session)
    investor_service = InvestorService(investor_repository)
    investor = investor_service.create_investor(name, email, phone_number, address)
    session.close()
    typer.echo(f"Investor {investor.name} added successfully")


@app.command()
def ls():
    """
    List all investors
    """
    investor_repository = InvestorRepository(session)
    investor_service = InvestorService(investor_repository)
    investors = investor_service.get_all_investors()
    session.close()

    table = Table(title="Investors")

    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")

    for investor in investors:
        table.add_row(str(investor.id), investor.name, investor.email)

    console.print(table)


@app.command()
def rm(investor_id: int):
    """
    Remove an investor

    Args:
        investor_id (int): ID of the investor
    """
    investor_repository = InvestorRepository(session)
    investor_service = InvestorService(investor_repository)
    investor_service.delete_investor(investor_id)
    session.close()
    typer.echo(f"Investor ID {investor_id} removed successfully")
