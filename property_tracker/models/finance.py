from enum import Enum as PyEnum

from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class FinancingType(PyEnum):
    """
    Represents the type of a financing agreement.
    """

    MORTGAGE = "Mortgage"


class Financing(Base):
    """
    Represents a financing agreement for the purchase of a property.
    """

    __tablename__ = "financings"
    id = Column(Integer, primary_key=True, index=True)
    financing_type = Column(Enum(FinancingType))
    start_date = Column(Date)
    end_date = Column(Date)
    interest_rate = Column(Float)
    loan_amount = Column(Float)
    property_id = Column(Integer, ForeignKey("properties.id"))
    investor_id = Column(Integer, ForeignKey("investors.id"))

    investor = relationship("Investor", back_populates="financings")
    property = relationship("Property", back_populates="financings")
    property_transactions = relationship("PropertyTransaction", back_populates="financing")


class Payment(Base):
    """
    Represents a payment made by a tenant to an investor for rent.
    """

    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    payment_date = Column(Date, nullable=False)
    payment_amount = Column(Float, nullable=False)
    payment_type = Column(String, nullable=False)
    notes = Column(String)
    financing_id = Column(Integer, ForeignKey("financings.id"))


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
    financing_id = Column(Integer, ForeignKey("financings.id"))

    property = relationship("Property", back_populates="property_transactions")
    financing = relationship("Financing", back_populates="property_transactions")


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
