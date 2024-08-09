from enum import Enum as PyEnum

from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class Mortgage(Base):
    """
    Represents a mortgage on a property.
    """

    __tablename__ = "mortgages"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    principal = Column(Float)
    payment_term = Column(Integer)
    annual_interest_rate = Column(Float)
    property_id = Column(Integer, ForeignKey("properties.id"))
    investor_id = Column(Integer, ForeignKey("investors.id"))

    investor = relationship("Investor", back_populates="mortgages")
    property = relationship("Property", back_populates="mortgages")
    property_transactions = relationship("PropertyTransaction", back_populates="mortgage")


class TransactionType(PyEnum):
    """
    Represents the type of a transaction.
    """

    PURCHASE = "Purchase"
    SALE = "Sale"
    REFINANCE = "Refinance"


class PropertyTransaction(Base):
    """
    Represents a transaction involving a property.
    """

    __tablename__ = "property_transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(Date, nullable=False)
    transaction_amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType))
    cash_payment = Column(Float)
    notes = Column(String)
    property_id = Column(Integer, ForeignKey("properties.id"))
    mortgage_id = Column(Integer, ForeignKey("mortgages.id"))

    property = relationship("Property", back_populates="property_transactions")
    mortgage = relationship("Mortgage", back_populates="property_transactions")


class PropertyOwnership(Base):
    """
    Represents an investor's ownership of a property.
    """

    __tablename__ = "property_ownerships"
    id = Column(Integer, primary_key=True, index=True)
    ownership_start_date = Column(Date, nullable=False)
    ownership_end_date = Column(Date)
    ownership_share = Column(Float, nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"))
    investor_id = Column(Integer, ForeignKey("investors.id"))
    transaction_id = Column(Integer, ForeignKey("property_transactions.id"))

    investor = relationship("Investor", back_populates="ownerships")
    property = relationship("Property", back_populates="ownerships")


class ValuationType(PyEnum):
    """
    Represents the type of a valuation.
    """

    PURCHASE = "Purchase"


class Valuation(Base):
    """
    Represents a valuation of a property.
    """

    __tablename__ = "valuations"
    id = Column(Integer, primary_key=True, index=True)
    valuation_date = Column(Date, nullable=False)
    valuation_amount = Column(Float, nullable=False)
    valuation_type = Column(Enum(ValuationType))
    property_id = Column(Integer, ForeignKey("properties.id"))

    property = relationship("Property", back_populates="valuations")


class Expense(Base):
    """
    Represents an expense incurred by an investor for a property.
    """

    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    date = Column(Date)
    investor_id = Column(Integer, ForeignKey("investors.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))

    investor = relationship("Investor", back_populates="expenses")
    property = relationship("Property", back_populates="expenses")


class RentalIncome(Base):
    """
    Represents a rent payment received for a property.
    """

    __tablename__ = "rental_incomes"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    date = Column(Date)
    property_id = Column(Integer, ForeignKey("properties.id"))
    investor_id = Column(Integer, ForeignKey("investors.id"))

    property = relationship("Property", back_populates="rental_income")
    investor = relationship("Investor", back_populates="rental_incomes")
