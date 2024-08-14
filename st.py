import pandas as pd
import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

from frontend.investor import show_investors
from frontend.property import show_properties
from frontend.simulate import show_simulate
from property_tracker.database import session
from property_tracker.repositories import FinanceRepository, InvestorRepository, PropertyRepository
from property_tracker.services import FinanceService, InvestorService, PropertyService
from property_tracker.services.simulate_v2 import (
    InvestmentDetails,
    InvestorType,
    MortgageCalculator,
    PropertyDetails,
    SimulationService,
    StampDutyCalculator,
)

st.set_page_config(layout="wide", page_title="Property Investment Tracker")

# Sidebar for navigation
st.sidebar.title("Property Investment Tracker")
page = st.sidebar.radio("Go to", ["Properties", "Investors", "Simulate"])

property_service = PropertyService(PropertyRepository(session))
investor_service = InvestorService(InvestorRepository(session))
finance_service = FinanceService(FinanceRepository(session), InvestorRepository(session))


# Navigation logic
if page == "Properties":
    show_properties(session)
elif page == "Investors":
    show_investors()
elif page == "Simulate":
    show_simulate()
