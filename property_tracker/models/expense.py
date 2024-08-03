from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class Expense(Base):
    """
    Represents an expense incurred by an investor for a property.
    """

    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    date = Column(Date)
