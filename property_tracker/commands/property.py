import typer
from rich.console import Console
from rich.table import Table

from property_tracker.database import session
from property_tracker.models.property import PropertyType, PurchaseCurrency, Status
from property_tracker.repositories import FinanceRepository, PropertyRepository
from property_tracker.services import PropertyService

app = typer.Typer()
console = Console()


@app.command()
def add(
    address: str,
    purchase_date: str,
    purchase_price: float,
    purchase_currency: PurchaseCurrency,
    prop_type: PropertyType,
    status: Status,
    investor_id: int,
):
    """
    Add a new property to the database.
    """
    property_service = PropertyService(PropertyRepository(session))
    property_service.create_property(
        address=address,
        purchase_date=purchase_date,
        purchase_price=purchase_price,
        purchase_currency=purchase_currency,
        property_type=prop_type,
        status=status,
        investor_id=investor_id,
    )
    console.print("Property added successfully.")
    session.close()


@app.command()
def ls():
    """
    List all properties.
    """
    property_service = PropertyService(PropertyRepository(session))
    properties = property_service.get_all_properties()
    table = Table(title="Properties")
    table.add_column("ID", style="cyan")
    table.add_column("Address")
    table.add_column("Purchase Date")
    table.add_column("Purchase Price")
    table.add_column("Purchase Currency")
    table.add_column("Type")
    table.add_column("Status")
    table.add_column("Owner ID")
    for prop in properties:
        table.add_row(
            str(prop.id),
            prop.address,
            str(prop.purchase_date),
            str(prop.purchase_price),
            prop.purchase_currency.value,
            prop.type.value,
            prop.status.value,
            str(prop.owner_id),
        )
    console.print(table)
    session.close()


@app.command()
def rm(property_id: int):
    """
    Remove a property from the database.
    """
    property_service = PropertyService(PropertyRepository(session))
    property_service.delete_property(property_id)
    console.print("Property removed successfully.")
    session.close()


@app.command()
def purchase(property_id: int, investor_id: int):
    """
    Buy a property.
    """
    finance_service = FinanceService(FinanceRepository(session))
