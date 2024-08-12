from dataclasses import dataclass
from enum import Enum as PyEnum
from typing import Dict, List, Tuple

import pandas as pd


class InvestorType(PyEnum):
    """
    Represents the type of an investor.
    Has implications on the tax treatment of the investor's income.
    """

    SOLE_TRADER = "Sole Trader"
    LIMITED_COMPANY = "Limited Company"


STAMP_DUTY_RULES: Dict[InvestorType, List[Tuple[int, float]]] = {
    InvestorType.SOLE_TRADER: [(0, 0.03), (250000, 0.08), (925000, 0.13), (1500000, 0.15)],
    InvestorType.LIMITED_COMPANY: [(0, 0.03), (125000, 0.05), (250000, 0.08), (925000, 0.13), (1500000, 0.15)],
}
PROPERTY_MANAGEMENT_CUT = 0.1
REPAIRS_AND_MAINTENANCE_CUT = 0.05


@dataclass
class PropertyDetails:
    """
    Represents the details of a property investment
    """

    purchase_price: float
    monthly_rent: float
    insurance: float
    service_charge: float
    ground_rent: float
    annual_price_appreciation: float
    annual_rent_appreciation: float

    def calculate_gross_yield(self) -> float:
        """
        Calculate the gross yield of the property

        :return: the gross yield
        """
        return (self.monthly_rent * 12) / self.purchase_price


@dataclass
class InvestmentDetails:
    """
    Represents the details of an investment
    """

    down_payment: float
    interest_rate: float
    payment_term: int
    legal_fees: float
    refurbishment_cost: float
    furnishing_cost: float

    def calculate_loan_amount(self, purchase_price: float) -> float:
        """
        Calculate the loan amount based on the purchase price and the down payment

        :param purchase_price: the purchase price of the property
        :return: the loan amount
        """
        return purchase_price - self.down_payment

    def calculate_total_cash_investment(self, stamp_duty: float) -> float:
        """
        Calculate the total cash investment

        :param stamp_duty: the stamp duty
        :return: the total cash investment
        """
        return self.down_payment + stamp_duty + self.legal_fees + self.refurbishment_cost + self.furnishing_cost


class MortgageCalculator:
    """
    A class to calculate mortgage-related metrics
    """

    @staticmethod
    def calculate_monthly_payment(principal: float, payment_term: int, annual_interest_rate: float) -> float:
        """
        Calculate the monthly mortgage payment

        :param principal: the principal amount
        :param payment_term: the payment term in years
        :param annual_interest_rate: the annual interest rate
        :return: the monthly mortgage payment
        """
        term_in_months = 12 * payment_term
        monthly_interest_rate = annual_interest_rate / 1200
        monthly_payment = principal * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -term_in_months)

        return monthly_payment

    @staticmethod
    def generate_payment_schedule(principal: float, payment_term: int, annual_interest_rate: float) -> pd.DataFrame:
        """
        Generate a mortgage payment schedule

        :param principal: the principal amount
        :param payment_term: the payment term in years
        :param annual_interest_rate: the annual interest rate
        :return: a DataFrame with the payment schedule
        """
        term_in_months = 12 * payment_term
        monthly_interest_rate = annual_interest_rate / 1200
        monthly_payment = MortgageCalculator.calculate_monthly_payment(principal, payment_term, annual_interest_rate)

        # create a payment schedule
        balance = principal
        payments = []
        for month in range(1, term_in_months + 1):
            interest = balance * monthly_interest_rate
            principal_payment = monthly_payment - interest
            balance -= principal_payment
            payments.append((month, interest, principal_payment, balance))

        payments = pd.DataFrame(payments, columns=["Month", "Interest", "Principal", "Balance"])
        # make the dataframe annual
        payments["Year"] = payments["Month"] // 12 + 1
        payments = (
            payments.groupby("Year").agg({"Interest": "sum", "Principal": "sum", "Balance": "last"}).reset_index()
        )
        # Add an ititial row for the start of the mortgage
        payments = pd.concat(
            [
                pd.DataFrame(
                    {
                        "Year": [0],
                        "Interest": [0],
                        "Principal": [0],
                        "Balance": [principal],
                    }
                ),
                payments,
            ]
        )

        # round the values to 1 decimal place
        payments = payments.round(2)

        return payments


class StampDutyCalculator:
    """
    A class to calculate stamp duty

    The stamp duty is a tax that is levied on the purchase of property in the UK.
    The amount of stamp duty payable depends on the purchase price of the property and the type of investor.
    """

    @staticmethod
    def calculate_stamp_duty(value: float, investor_type: InvestorType) -> float:
        """
        Calculate the stamp duty payable on a property purchase

        :param value: the purchase price of the property
        :param investor_type: the type of investor
        :return: the stamp duty payable
        """

        def calculate_duty(brackets_and_rates: List[Tuple[int, float]]) -> float:
            duty = 0
            for i, (bracket, rate) in enumerate(brackets_and_rates):
                if i + 1 < len(brackets_and_rates):
                    next_bracket = brackets_and_rates[i + 1][0]
                    if value > bracket:
                        duty += (min(value, next_bracket) - bracket) * rate
                    else:
                        break
                else:
                    duty += (value - bracket) * rate
            return duty

        return calculate_duty(STAMP_DUTY_RULES[investor_type])


@dataclass
class RunningCostsCalculator:
    """
    A class to calculate the running costs of a property

    The running costs include the mortgage payment, insurance, service charge, ground rent, property management fee,
    and repairs and maintenance.
    """

    property_management_cut: float
    repairs_and_maintenance_cut: float

    def calculate_running_costs(
        self, mortgage_payment: float, monthly_rent: float, insurance: float, service_charge: float, ground_rent: float
    ) -> float:
        """
        Calculate the running costs of a property

        :param mortgage_payment: the monthly mortgage payment
        :param monthly_rent: the monthly rent
        :param insurance: the monthly insurance cost
        :param service_charge: the monthly service charge
        :param ground_rent: the monthly ground rent
        :return: the total running costs
        """
        property_mgmt_fee = monthly_rent * self.property_management_cut
        repairs_and_maintenance = monthly_rent * self.repairs_and_maintenance_cut

        return mortgage_payment + insurance + service_charge + ground_rent + property_mgmt_fee + repairs_and_maintenance


class RentalIncomeCalculator:
    """
    A class to calculate rental income metrics
    """

    @staticmethod
    def calculate_monthly_rental_income(monthly_rent: float, running_costs: float) -> float:
        """
        Calculate the monthly rental income after deducting the running costs

        :param monthly_rent: the monthly rent
        :param running_costs: the monthly running costs
        """
        return monthly_rent - running_costs

    @staticmethod
    def calculate_annual_cash_flow(monthly_rental_income: float) -> float:
        """
        Calculate the annual cash flow

        :param monthly_rental_income: the monthly rental income
        :return: the annual cash flow
        """
        return monthly_rental_income * 12


class EquityGrowthCalculator:
    """
    A class to calculate equity growth metrics
    """

    @staticmethod
    def forecast_property_value_appreciation(
        purchase_price: float, annual_price_appreciation: float, years: int
    ) -> float:
        """
        Forecast the future value of a property based on the annual price appreciation

        :param purchase_price: the purchase price of the property
        :param annual_price_appreciation: the annual price appreciation
        :param years: the number of years to forecast
        :return: the forecasted property value
        """
        return purchase_price * (1 + annual_price_appreciation) ** years

    @staticmethod
    def calculate_equity_growth(future_property_value: float, payment_schedule: pd.DataFrame, year: int) -> float:
        """
        Calculate the equity growth of a property investment at a given year in the future

        :param principal: the principal amount of the mortgage
        :param annual_price_appreciation: the annual price appreciation of the property
        :param payment_schedule: the mortgage payment schedule
        :param year: the year in the future
        :return: the equity growth
        """
        final_balance = payment_schedule.loc[year, "Balance"]
        equity_growth = future_property_value - final_balance
        return equity_growth


class InvestmentMetricsCalculator:
    """
    A class to calculate investment metrics
    """

    @staticmethod
    def calculate_net_yield(annual_cash_flow: float, purchase_price: float) -> float:
        """
        Calculate the net yield.

        :param annual_cash_flow: the annual cash flow
        :param purchase_price: the purchase price of the property
        :return: the net yield
        """
        return annual_cash_flow / purchase_price

    @staticmethod
    def calculate_rental_roi(annual_cash_flow: float, total_cash_investment: float) -> float:
        """
        Calculate the return on investment (ROI) of rental income

        :param annual_cash_flow: the annual cash flow
        :param total_cash_investment: the total cash investment
        :return: the ROI
        """
        return annual_cash_flow / total_cash_investment

    @staticmethod
    def calculate_equity_roi(equity_growth: float, total_cash_investment: float) -> float:
        """
        Calculate the return on investment (ROI) of equity growth

        :param equity_growth: the equity growth
        :param total_cash_investment: the total cash investment
        :return: the ROI
        """
        return equity_growth / total_cash_investment


class SimulationService:
    """
    A service to run simulations of property investments
    """

    def run_simulation(
        self,
        property_details: PropertyDetails,
        investment_details: InvestmentDetails,
        investor_type: InvestorType,
        number_of_years: int,
    ) -> Tuple[float, pd.DataFrame, float, float]:
        """
        Run a simulation of a property investment

        :param property_details: the details of the property investment
        :param investment_details: the details of the investment
        :param investor_type: the type of investor
        :return: a tuple containing the total cash investment, the mortgage payment schedule, the gross yield,
        and the net yield
        """

        yearly_metrics = []

        # Calculate the stamp duty
        stamp_duty = StampDutyCalculator.calculate_stamp_duty(property_details.purchase_price, investor_type)

        # Calculate the loan amount
        loan_amount = investment_details.calculate_loan_amount(property_details.purchase_price)

        # Calculate the monthly mortgage payment
        mortgage_payment = MortgageCalculator.calculate_monthly_payment(
            loan_amount, investment_details.payment_term, investment_details.interest_rate
        )

        # Generate the mortgage payment schedule
        payment_schedule = MortgageCalculator.generate_payment_schedule(
            loan_amount, investment_details.payment_term, investment_details.interest_rate
        )

        # Calculate the running costs
        running_costs = RunningCostsCalculator(
            property_management_cut=PROPERTY_MANAGEMENT_CUT, repairs_and_maintenance_cut=REPAIRS_AND_MAINTENANCE_CUT
        ).calculate_running_costs(
            mortgage_payment,
            property_details.monthly_rent,
            property_details.insurance,
            property_details.service_charge,
            property_details.ground_rent,
        )

        # Calculate the monthly rental income
        monthly_rental_income = RentalIncomeCalculator.calculate_monthly_rental_income(
            property_details.monthly_rent, running_costs
        )

        # Calculate the annual cash flow
        annual_cash_flow = RentalIncomeCalculator.calculate_annual_cash_flow(monthly_rental_income)

        # Calculate the gross yield
        gross_yield = property_details.calculate_gross_yield()
        # Calculate the net yield
        net_yield = InvestmentMetricsCalculator.calculate_net_yield(annual_cash_flow, property_details.purchase_price)

        # Calculate the total cash investment
        total_cash_investment = investment_details.calculate_total_cash_investment(stamp_duty)

        # Calculate the ROI
        rental_roi = InvestmentMetricsCalculator.calculate_rental_roi(annual_cash_flow, total_cash_investment)

        yearly_metrics.append(
            {
                "Year": 0,
                "Gross Yield": gross_yield,
                "Net Yield": net_yield,
                "Rental ROI": f"{rental_roi:.2%}",
                "equity": f"£{investment_details.down_payment/1000:.0f}K",
            }
        )

        property_value = property_details.purchase_price
        for year in range(1, number_of_years):

            equity_growth = EquityGrowthCalculator.calculate_equity_growth(property_value, payment_schedule, year)

            future_running_costs = running_costs * (1 + property_details.annual_rent_appreciation) ** year
            future_monthly_rent = (
                property_details.monthly_rent * (1 + property_details.annual_rent_appreciation) ** year
            )

            # Calculate the monthly rental income
            monthly_rental_income = RentalIncomeCalculator.calculate_monthly_rental_income(
                future_monthly_rent, future_running_costs
            )
            # Calculate the annual cash flow
            annual_cash_flow = RentalIncomeCalculator.calculate_annual_cash_flow(monthly_rental_income)

            # Calculate the ROI
            rental_roi = InvestmentMetricsCalculator.calculate_rental_roi(annual_cash_flow, total_cash_investment)

            # Show equity growth as £ and human readable money format, cast as string like so "£100K"
            equity_growth = f"£{equity_growth/1000:.0f}K"

            yearly_metrics.append(
                {
                    "Year": year,
                    "Gross Yield": gross_yield,
                    "Net Yield": net_yield,
                    "Rental ROI": f"{rental_roi:.2%}",
                    "equity": equity_growth,
                }
            )

        yearly_metrics = pd.DataFrame(yearly_metrics)

        return total_cash_investment, mortgage_payment, yearly_metrics
