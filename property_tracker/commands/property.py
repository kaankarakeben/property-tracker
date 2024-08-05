import typer
from rich.console import Console
from rich.table import Table

from property_tracker.database import session
from property_tracker.models.property import PropertyType, PurchaseCurrency, Status
from property_tracker.repositories import FinanceRepository, PropertyRepository
from property_tracker.services import FinanceService, PropertyService

app = typer.Typer()
console = Console()


@app.command()
def add(
    address: str,
    postcode: str,
    city: str,
    purchase_date: str,
    purchase_price: float,
    purchase_currency: PurchaseCurrency,
    description: str,
    no_of_bedrooms: int,
    no_of_bathrooms: int,
    sqm: float,
    floor: int,
    furnished: bool,
    property_type: PropertyType,
    status: Status,
):
    """
    Add a new property.
    """

    property_service = PropertyService(PropertyRepository(session))
    property = property_service.create_property(
        address,
        postcode,
        city,
        purchase_date,
        purchase_price,
        purchase_currency,
        description,
        no_of_bedrooms,
        no_of_bathrooms,
        sqm,
        floor,
        furnished,
        property_type,
        status,
    )
    session.close()
    console.print(f"Property {property.address} added successfully.")


@app.command()
def ls():
    """
    List all properties.
    """
    property_service = PropertyService(PropertyRepository(session))
    inv_properties = property_service.get_all_properties()
    table = Table(title="Properties")
    table.add_column("ID", style="cyan")
    table.add_column("Address")
    table.add_column("City")
    table.add_column("Type")
    table.add_column("Status")
    table.add_column("Purchase Price")
    table.add_column("Currency")
    table.add_column("Purchase Date")
    table.add_column("Bedrooms")
    table.add_column("Bathrooms")
    table.add_column("SQM")
    table.add_column("Floor")
    table.add_column("Furnished")

    for inv_property in inv_properties:
        table.add_row(
            str(inv_property.id),
            inv_property.address,
            inv_property.city,
            inv_property.property_type.value,
            inv_property.status.value,
            str(inv_property.purchase_price),
            inv_property.purchase_currency.value,
            str(inv_property.purchase_date),
            str(inv_property.no_of_bedrooms),
            str(inv_property.no_of_bathrooms),
            str(inv_property.sqm),
            str(inv_property.floor),
            str(inv_property.furnished),
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
def purchase(
    property_id: int,
    investor_id: int,
    transaction_date: str,
    transaction_amount: float,
    transaction_notes: str,
    cash_payment: float,
    ownership_share: float,
    financing_interest_rate: float,
    financing_loan_amount: float,
):
    """
    Purchase a property.
    """

    finance_service = FinanceService(FinanceRepository(session))
    finance_service.purchase_property(
        property_id,
        investor_id,
        transaction_date,
        transaction_amount,
        transaction_notes,
        cash_payment,
        ownership_share,
        financing_interest_rate,
        financing_loan_amount,
    )
    session.close()
    console.print("Property purchased successfully.")
