from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class InvestorType(PyEnum):
    """
    Represents the type of an investor.
    Has implications on the tax treatment of the investor's income.
    """

    SOLE_TRADER = "Sole Trader"
    LIMITED_COMPANY = "Limited Company"


class Investor(Base):
    """
    Represents an investor in the property investment tracker.
    """

    __tablename__ = "investors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    investor_type = Column(Enum(InvestorType), nullable=False)
    company_name = Column(String)

    financings = relationship("Financing", back_populates="investor")
    ownerships = relationship("PropertyOwnership", back_populates="investor")
