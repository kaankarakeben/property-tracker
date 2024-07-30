"""
This module contains the SQLAlchemy models for the property investment tracker.
"""

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql://postgres:password@localhost/property_investment"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Investor(Base):
    """
    Represents an investor in the property investment tracker.
    """

    __tablename__ = "investors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_details = Column(String)
    portfolio_value = Column(Float)


class Property(Base):
    """
    Represents a property that an investor owns and rents out.
    """

    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    purchase_date = Column(Date)
    purchase_price = Column(Float)
    current_market_value = Column(Float)
    type = Column(String)
    status = Column(String)


class Tenant(Base):
    """
    Represents a tenant who rents a property from an investor.
    """

    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_details = Column(String)


class Lease(Base):
    """
    Represents a lease agreement between a tenant and an investor for a property.
    """

    __tablename__ = "leases"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    lease_start_date = Column(Date)
    lease_end_date = Column(Date)
    monthly_rent = Column(Float)
    deposit_amount = Column(Float)

    property = relationship("Property")
    tenant = relationship("Tenant")


class MaintenanceRequest(Base):
    """
    Represents a maintenance request for a property by a tenant.
    """

    __tablename__ = "maintenance_requests"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    request_date = Column(Date)
    description = Column(String)
    status = Column(String)
    cost = Column(Float)

    property = relationship("Property")


class Payment(Base):
    """
    Represents a payment made by a tenant to an investor for rent.
    """

    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    lease_id = Column(Integer, ForeignKey("leases.id"))
    payment_date = Column(Date)
    amount = Column(Float)
    payment_type = Column(String)

    tenant = relationship("Tenant")
    lease = relationship("Lease")


class Expense(Base):
    """
    Represents an expense incurred by an investor for a property.
    """

    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    date = Column(Date)
    description = Column(String)
    amount = Column(Float)
    expense_type = Column(String)

    property = relationship("Property")


class TaxPayment(Base):
    """
    Represents a tax payment made by an investor for a property.
    """

    __tablename__ = "tax_payments"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    tax_year = Column(Integer)
    amount = Column(Float)
    payment_date = Column(Date)
    tax_type = Column(String)

    property = relationship("Property")


# Create all tables
Base.metadata.create_all(bind=engine)
