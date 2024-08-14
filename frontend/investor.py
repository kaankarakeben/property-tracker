import pandas as pd
import streamlit as st

from property_tracker.repositories import InvestorRepository
from property_tracker.services import InvestorService


def show_investors(session):
    investor_service = InvestorService(InvestorRepository(session))
    st.write("### Investors")
    investors = investor_service.get_all_investors()
    investors_df = pd.DataFrame([investor.__dict__ for investor in investors])
    st.dataframe(investors_df, hide_index=True)
