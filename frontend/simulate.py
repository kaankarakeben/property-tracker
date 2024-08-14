import streamlit as st

from property_tracker.services.simulate_v2 import (
    InvestmentDetails,
    InvestorType,
    MortgageCalculator,
    PropertyDetails,
    SimulationService,
)

simulation_service = SimulationService()


def show_simulate():
    st.write("### Simulate")
    # Create container for simulation form
    simulation_container = st.container()
    with simulation_container:

        # Create a form to get the property details
        st.write("#### Property Details")

        purchase_price = st.number_input("Purchase Price", value=0)
        monthly_rent = st.number_input("Monthly Rent", value=0)
        insurance = st.number_input("Insurance", value=0)
        service_charge = st.number_input("Service Charge", value=0)
        ground_rent = st.number_input("Ground Rent", value=0)
        annual_price_appreciation = st.number_input("Annual Price Appreciation (%)", value=0)
        annual_rent_appreciation = st.number_input("Annual Rent Appreciation (%)", value=0)

        property_details = PropertyDetails(
            purchase_price=purchase_price,
            monthly_rent=monthly_rent,
            insurance=insurance,
            service_charge=service_charge,
            ground_rent=ground_rent,
            annual_price_appreciation=annual_price_appreciation,
            annual_rent_appreciation=annual_rent_appreciation,
        )

        # Create a form to get the investment details
        st.write("#### Investment Details")
        down_payment = st.number_input("Down Payment", value=0)
        interest_rate = st.number_input("Interest Rate (%)", value=0)
        payment_term = st.number_input("Payment Term (years)", value=0)
        legal_fees = st.number_input("Legal Fees", value=0)
        refurbishment_costs = st.number_input("Refurbishment Costs", value=0)
        furnishing_costs = st.number_input("Furnishing Costs", value=0)

        investment_details = InvestmentDetails(
            down_payment=down_payment,
            interest_rate=interest_rate,
            payment_term=payment_term,
            legal_fees=legal_fees,
            refurbishment_cost=refurbishment_costs,
            furnishing_cost=furnishing_costs,
        )

        # Select investor type and number of years to simulate
        st.write("#### Simulation Details")
        investor_type = st.selectbox("Investor Type", [InvestorType.SOLE_TRADER, InvestorType.LIMITED_COMPANY])
        num_years = st.number_input("Number of Years", value=0)

        # Add a button to run the simulation
        run_simulation = st.button("Run Simulation")

        if run_simulation:
            total_cash_investment, mortgage_payment, yearly_metrics = simulation_service.run_simulation(
                property_details=property_details,
                investment_details=investment_details,
                investor_type=investor_type,
                num_years=num_years,
            )

            # Display the simulation results
            st.write("#### Simulation Results")
            st.write(f"Total Cash Investment: £{total_cash_investment}")
            st.write(f"Mortgage Payment: £{mortgage_payment}")
            st.write("Yearly Metrics")
            yearly_metrics_df = yearly_metrics.reset_index()
            st.dataframe(yearly_metrics_df, hide_index=True)
