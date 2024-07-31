from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from property_tracker.models import Base

DATABASE_URL = "postgresql://postgres:password@localhost/property_investment"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
