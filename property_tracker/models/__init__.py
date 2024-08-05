from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:password@localhost/property_investment"
engine = create_engine(DATABASE_URL)
Base = declarative_base()


from property_tracker.models.finance import (
    Expense,
    Financing,
    Payment,
    PropertyOwnership,
    PropertyTransaction,
    Valuation,
)
from property_tracker.models.investor import Investor
from property_tracker.models.property import Property
