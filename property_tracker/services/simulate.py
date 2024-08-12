from enum import Enum as PyEnum

import pandas as pd


class InvestorType(PyEnum):
    """
    Represents the type of an investor.
    Has implications on the tax treatment of the investor's income.
    """

    SOLE_TRADER = "Sole Trader"
    LIMITED_COMPANY = "Limited Company"


def calculate_stamp_duty(value, investor_type: InvestorType):
    """
    Calculate the stamp duty for a property purchase
    """

    # Initialize the total stamp duty
    total_duty = 0

    # Determine the rate based on ownership type
    if investor_type == InvestorType.SOLE_TRADER:
        if value <= 250000:
            total_duty += value * 0.03
        elif value <= 925000:
            total_duty += 250000 * 0.03 + (value - 250000) * 0.08
        elif value <= 1500000:
            total_duty += 250000 * 0.03 + 675000 * 0.08 + (value - 925000) * 0.13
        else:
            total_duty += 250000 * 0.03 + 675000 * 0.08 + 575000 * 0.13 + (value - 1500000) * 0.15
    elif investor_type == InvestorType.LIMITED_COMPANY:
        if value <= 125000:
            total_duty += value * 0.03
        elif value <= 250000:
            total_duty += 125000 * 0.03 + (value - 125000) * 0.05
        elif value <= 925000:
            total_duty += 125000 * 0.03 + 125000 * 0.05 + (value - 250000) * 0.08
        elif value <= 1500000:
            total_duty += 125000 * 0.03 + 125000 * 0.05 + 675000 * 0.08 + (value - 925000) * 0.13
        else:
            total_duty += 125000 * 0.03 + 125000 * 0.05 + 675000 * 0.08 + 575000 * 0.13 + (value - 1500000) * 0.15

    return total_duty


class SimulationService:
    """Service for simulating a property investment"""

    @staticmethod
    def get_monthly_payment(principal, payment_term, annual_interest_rate):
        """
        Calculate the monthly payment of a mortage

        :param principal: the amount of the loan
        :param payment_term: the term of the loan in years
        :param annual_interest_rate: the annual interest rate
        """

        term_in_months = 12 * payment_term
        monthly_interest_rate = annual_interest_rate / 1200
        monthly_payment = principal * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -term_in_months)

        return monthly_payment

    @staticmethod
    def mortage_calculator(principal, payment_term, annual_interest_rate):
        """
        Calculate the monthly payment of a mortage

        :param principal: the amount of the loan
        :param payment_term: the term of the loan in years
        :param annual_interest_rate: the annual interest rate
        """

        term_in_months = 12 * payment_term
        monthly_interest_rate = annual_interest_rate / 1200
        monthly_payment = SimulationService.get_monthly_payment(principal, payment_term, annual_interest_rate)

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
        payments["Total Payment"] = payments["Interest"] + payments["Principal"]
        payments["Cumulative Interest"] = payments["Interest"].cumsum()
        payments["Cumulative Principal"] = payments["Principal"].cumsum()
        payments["Cumulative Total Payment"] = payments["Total Payment"].cumsum()

        # decimals to 2
        payments = payments.round(2)

        return payments

    def calculate_running_costs(
        self,
        mortgage_payment,
        monthly_rent,
        insurance,
        service_charge,
        ground_rent,
        property_management_cut,
        repairs_and_maintenance_cut,
    ):
        """
        Calculate the monthly running costs for the property

        :param mortgage_payment: the monthly mortgage payment
        :param monthly_rent: the monthly rent
        :param insurance: the monthly insurance cost
        :param service_charge: the monthly service charge
        :param ground_rent: the monthly ground rent
        :param property_management_cut: the monthly property management cut
        :param repairs_maintenance: the monthly repairs and maintenance cost
        :param voids: the monthly voids cost
        """
        property_mgmt_fee = monthly_rent * property_management_cut
        repairs_and_maintenance = monthly_rent * repairs_and_maintenance_cut

        return mortgage_payment + insurance + service_charge + ground_rent + property_mgmt_fee + repairs_and_maintenance

    def calculate_monthly_rental_income(self, monthly_rent, running_costs):
        """
        Calculate the monthly rental income after deducting the running costs

        :param monthly_rent: the monthly rent
        :param running_costs: the monthly running costs
        """
        return monthly_rent - running_costs

    def calculate_metrics(
        down_payment,
        stamp_duty,
        legal_fees,
        refurbishment_cost,
        furnishing_cost,
        monthly_rental_income,
        purchase_price,
        monthly_rent,
    ):

        # Calculate the total cash investment
        total_cash_investment = down_payment + stamp_duty + legal_fees + refurbishment_cost + furnishing_cost
        # Calculate annual cash flow
        annual_cash_flow = monthly_rental_income * 12
        # Gross yield
        gross_yield = (monthly_rent * 12) / purchase_price
        # Net yield
        net_yield = annual_cash_flow / total_cash_investment
        # ROI
        roi = annual_cash_flow / total_cash_investment

        print(f"Total cash investment: £{total_cash_investment}")
        print(f"Annual cash flow: £{annual_cash_flow:.2f}")
        print(f"Gross yield: {gross_yield:.2%}")
        print(f"Net yield: {net_yield:.2%}")
        print(f"ROI: {roi:.2%}")

        return total_cash_investment, annual_cash_flow, gross_yield, net_yield, roi

    def run(
        self,
        investor_type,
        purchase_price,
        down_payment,
        interest_rate,
        payment_term,
        monthly_rent,
        insurance,
        service_charge,
        ground_rent,
        property_management_cut,
        repairs_and_maintenance_cut,
        legal_fees,
        refurbishment_cost,
        furnishing_cost,
    ):
        # Calculate stamp duty
        stamp_duty = calculate_stamp_duty(purchase_price, investor_type)
        # Calculate the loan amount
        loan_amount = purchase_price - down_payment
        # Calculate the monthly payment
        monthly_payment, payment_schedule = self.mortage_calculator(loan_amount, payment_term, interest_rate)
        # Calculate the running costs
        running_costs = self.calculate_running_costs(
            monthly_payment,
            monthly_rent,
            insurance,
            service_charge,
            ground_rent,
            property_management_cut,
            repairs_and_maintenance_cut,
        )
        # Calculate the monthly rental income
        monthly_rental_income = self.calculate_monthly_rental_income(monthly_rent, running_costs)
        # Calculate the metrics
        total_cash_investment, annual_cash_flow, gross_yield, net_yield, roi = self.calculate_metrics(
            down_payment,
            stamp_duty,
            legal_fees,
            refurbishment_cost,
            furnishing_cost,
            monthly_rental_income,
            purchase_price,
            monthly_rent,
        )

        return monthly_payment, payment_schedule, running_costs, monthly_rental_income
