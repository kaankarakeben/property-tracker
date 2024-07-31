from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class Payment(Base):
    """
    Represents a payment made by a tenant to an investor for rent.
    """

    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    date = Column(Date)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    investor_id = Column(Integer, ForeignKey("investors.id"))
    investor = relationship("Investor", back_populates="payments")
