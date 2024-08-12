import datetime

import typer
from rich import print as rprint
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from property_tracker.database import session
from property_tracker.repositories import FinanceRepository, InvestorRepository, PropertyRepository
from property_tracker.services import FinanceService, InvestorService, PropertyService

app = typer.Typer()
console = Console()

investor_repository = InvestorRepository(session)
property_repository = PropertyRepository(session)
finance_repository = FinanceRepository(session)
investor_service = InvestorService(investor_repository)
property_service = PropertyService(property_repository)
finance_service = FinanceService(finance_repository, investor_repository)

LTV = 0.75
LEGAL_FEES = 2000
PROPERTY_MANAGEMENT_CUT = 0.12
REPAIRS_PCT = 0.05
VOID_WEEKS_PER_YEAR = 2
PAYMENT_TERM = 20


def user_continue():
    """Ask the user to continue by pressing any key"""
    console.input("Press [bold yellow]Enter[/bold yellow] to continue...")
    console.print()


def show_information_panel(title, markdown_text, show_continue=True):
    """Show an information panel to the user"""
    rprint(
        Panel(
            Markdown(markdown_text),
            title=Text(title, style="bold"),
            title_align="left",
        )
    )
    if show_continue:
        user_continue()


def check_down_payment_inline_LTV(down_payment, purchase_price):
    """Check if the down payment is inline with the LTV"""
    if down_payment < purchase_price * (1 - LTV):
        show_information_panel(
            "Down Payment Too Low",
            f"""
            The down payment is too low for the loan to value ratio of {LTV * 100}%. 
            The minimum down payment should be £{int(purchase_price * (1 - LTV))}K.
            """,
        )
        return False
    return True


@app.command()
def run(investor_id: int, property_id: int, investment_type: str):
    """
    Run the property investment simulation
    """

    show_information_panel(
        "Property Investment Simulation",
        """
        This command will simulate the investment of a property by an investor. 
        The simulation will calculate the total investment amount, the stamp duty, and the legal fees.
        """,
    )

    investor = investor_service.get_investor(investor_id)
    property = property_service.get_property(property_id)

    if not investor:
        show_information_panel("Investor Not Found", "The investor with the specified ID was not found.")
        return

    if not property:
        show_information_panel("Property Not Found", "The property with the specified ID was not found.")
        return

    show_information_panel(
        "Investor Information",
        f"""
        - **Name**: {investor.first_name} {investor.last_name}
        - **Email**: {investor.email}
        - **Phone Number**: {investor.phone_number}
        - **Address**: {investor.address}
        - **Investor Type**: {investor.investor_type}
        - **Company Name**: {investor.company_name}
        """,
    )

    show_information_panel(
        "Property Information",
        f"""
        - **Address**: {property.address}
        - **Postcode**: {property.postcode}
        - **City**: {property.city}
        - **Description**: {property.description}
        - **Number of Bedrooms**: {property.no_of_bedrooms}
        - **Number of Bathrooms**: {property.no_of_bathrooms}
        - **SQM**: {property.sqm}
        - **Floor**: {property.floor}
        - **Furnished**: {property.furnished}
        - **Property Type**: {property.property_type}
        - **Investment Type**: {investment_type}
        """,
    )

    # Go through some of the assumptions we are making
    # in the simulation process; LTV, legal fees, property management pct cut, repairs pct and voids in a year
    show_information_panel(
        "Assumptions",
        f"""
        - **Loan to Value (LTV)**: {LTV}
        - **Legal Fees**: £{LEGAL_FEES}
        - **Property Management Cut**: {PROPERTY_MANAGEMENT_CUT * 100}%
        - **Repairs Percentage**: {REPAIRS_PCT * 100}%
        - **Voids per Year (weeks)**: {VOID_WEEKS_PER_YEAR}
        """,
    )

    # Ask for purchase price
    purchase_price = Prompt.ask("Enter the purchase price of the property (e.g. 500 for £500K)")
    purchase_price = float(purchase_price)
    # Ask for down payment
    down_payment = Prompt.ask("Enter the down payment amount (e.g. 100 for £100K)")
    down_payment = float(down_payment)
    # Confirm that down payment is inline with LTV
    if not check_down_payment_inline_LTV(down_payment, purchase_price):
        # Show the min down payment required and continue with the simulation
        min_down_payment = purchase_price * (1 - LTV)
        down_payment_continue = Confirm.ask(
            f"The minimum down payment should be £{min_down_payment}K. Do you want to continue with this amount?"
        )
        if not down_payment_continue:
            return
        else:
            down_payment = min_down_payment

    # Confirm  that loan amount is correct
    loan_amount = purchase_price - down_payment
    rprint(f"The loan amount is: [bold green]£{int(loan_amount)}K[/bold green]")
    # Ask for the current interest rate
    interest_rate = Prompt.ask("Enter the current interest rate (e.g. 3 for 3%)")
    interest_rate = float(interest_rate)
    # Ask for the term of the loan
    payment_term = Prompt.ask("Enter the term of the loan in years (e.g. 20 for 20 years)")
    payment_term = int(payment_term)

    # turn interest rate into a decimal
    interest_rate = interest_rate / 100

    # Use today's date
    transaction_date = datetime.date.today().strftime("%Y-%m-%d")
    finance_service.purchase_property(
        property_id=property_id,
        investor_id=investor_id,
        transaction_date=transaction_date,
        transaction_amount=purchase_price * 1000,
        transaction_notes=f"Property purchase for {investment_type}",
        cash_payment=down_payment,
        ownership_share=100,
        annual_interest_rate=interest_rate,
        principal=loan_amount,
        payment_term=payment_term,
    )

    # Get the expenses for the property purchase
    expenses = finance_service.get_all_expenses(property_id)
    # Get the cost of stamp duty
    stamp_duty = sum([expense.amount for expense in expenses if expense.description == "Stamp Duty"])
    legal_fees = sum([expense.amount for expense in expenses if expense.description == "Legal Fees"])

    show_information_panel(
        "Property Purchased",
        f"""
        The property has been successfully purchased by the investor.
        - **Transaction Date**: {transaction_date}
        - **Purchase Price**: £{int(purchase_price)}K
        - **Legal Fees**: £{LEGAL_FEES}
        - **Stamp Duty**: £{int(stamp_duty)}K

        # Mortgage Details
        - **LTV**: "{(loan_amount / purchase_price) * 100}%"
        - **Down Payment**: £{int(down_payment)}K
        - **Loan Amount**: £{int(loan_amount)}K
        - **Interest Rate**: "{interest_rate * 100}%"
        - **Payment Term**: {payment_term} years
        """,
    )

    # Ask how much is the investor looking to spend to get the property ready for rent
    refurbishment_cost = Prompt.ask("Enter the refurbishment cost for the property")
    refurbishment_cost = float(refurbishment_cost)

    # Furnishing the property
    furnishing_cost = Prompt.ask("Enter the cost of furnishing the property")
    furnishing_cost = float(furnishing_cost)

    # Ask for the monthly rent
    monthly_rent = Prompt.ask("Enter the monthly rent you are expecting for the property")
    monthly_rent = float(monthly_rent)

    # Ask for the running costs
    running_costs = Prompt.ask(
        "Enter the monthly running costs for the property. These include insurance, service charges etc."
    )
    running_costs = float(running_costs)

    show_information_panel(
        "Property Investment Summary",
        f"""
        - **Total Cash Investment**: £{int(total_cash_investment)}K
        - **Annual Cash Flow**: £{int(annual_cash_flow)}
        - **Gross Yield**: {gross_yield * 100}%
        - **Net Yield**: {net_yield * 100}%
        - **ROI**: {roi * 100}%
        """,
    )
