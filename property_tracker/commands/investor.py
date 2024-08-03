import typer
from rich.console import Console
from rich.table import Table

from property_tracker.database import session
from property_tracker.repositories import InvestorRepository
from property_tracker.services import InvestorService

app = typer.Typer()
console = Console()


@app.command()
def add(
    first_name: str, last_name: str, email: str, phone_number: str, address: str, investor_type: str, company_name: str
):
    """
    Add a new investor

    Args:
        first_name (str): First name of the investor
        last_name (str): Last name of the investor
        email (str): Email of the investor
        phone_number (str): Phone number of the investor
        address (str): Address of the investor
        investor_type (str): Type of the investor
        company_name (str): Name of the company
    """
    investor_repository = InvestorRepository(session)
    investor_service = InvestorService(investor_repository)
    investor = investor_service.create_investor(
        first_name, last_name, email, phone_number, address, investor_type, company_name
    )
    session.close()
    typer.echo(f"Investor {investor.first_name} {investor.last_name} added successfully")


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
    table.add_column("First Name", style="magenta")
    table.add_column("Last Name", style="yellow")
    table.add_column("Email", style="green")
    table.add_column("Phone Number", style="blue")
    table.add_column("Address", style="red")
    table.add_column("Investor Type", style="cyan")
    table.add_column("Company Name", style="magenta")

    for investor in investors:
        table.add_row(
            str(investor.id),
            investor.first_name,
            investor.last_name,
            investor.email,
            investor.phone_number,
            investor.address,
            investor.investor_type.value,
            investor.company_name,
        )

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
