from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from property_tracker.models import Base

engine = create_engine("sqlite:///property_tracker.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
