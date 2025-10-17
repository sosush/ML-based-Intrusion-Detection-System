from sqlalchemy import create_engine, Column, Integer, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///instance/database.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    label = Column(Integer)
    proba = Column(Float)
    anomaly = Column(Float)
    cluster = Column(Integer)
    risk = Column(Float)
    features = Column(JSON)

def init_db():
    Base.metadata.create_all(bind=engine)
