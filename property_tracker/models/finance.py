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
    financing_type = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    interest_rate = Column(Float)
    loan_amount = Column(Float)
    property_id = Column(Integer, ForeignKey("properties.id"))
    investor_id = Column(Integer, ForeignKey("investors.id"))
    property = relationship("Property", back_populates="financing")
    investor = relationship("Investor", back_populates="financing")


class Payments(Base):
    """
    Represents a payment made by a tenant to an investor for rent.
    """

    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    payment_date = Column(Date, nullable=False)
    payment_amount = Column(Float, nullable=False)
    payment_type = Column(String, nullable=False)
    notes = Column(String)
    financing = relationship("Financing", back_populates="payments")


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
    transaction_type = Column(String, nullable=False)
    cash_payment = Column(Float)
    notes = Column(String)
    property = relationship("Property", back_populates="transactions")
    financing = relationship("Financing", back_populates="transactions")


class PropertyOwnership(Base):
    """
    Represents an investor's ownership of a property.
    """

    __tablename__ = "property_investors"
    id = Column(Integer, primary_key=True, index=True)
    ownership_start_date = Column(Date, nullable=False)
    ownership_end_date = Column(Date)
    ownership_share = Column(Float, nullable=False)
    property = relationship("Property", back_populates="investors")
    investor = relationship("Investor", back_populates="properties")
    transaction = relationship("PropertyTransaction", back_populates="ownership")


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
    property = relationship("Property", back_populates="valuations")


class Lease(Base):
    """
    Represents a lease agreement between a tenant and an investor for a property.
    """

    __tablename__ = "leases"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    rent_amount = Column(Float)
    deposit_amount = Column(Float)
    investor = relationship("Investor", back_populates="leases")
    property = relationship("Property", back_populates="leases")
    tenant = relationship("Tenant", back_populates="leases")
