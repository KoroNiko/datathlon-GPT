from sqlalchemy import BigInteger, CheckConstraint, Column, Date, DateTime, Float, ForeignKey, Index, Integer, \
    String, Table, Time, text, select, JSON

from sqlalchemy.dialects.sqlite import INTEGER, NUMERIC, REAL, TEXT, DATETIME


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Artist(Base):
    __tablename__ = 'Artist'
    
    id = Column(INTEGER, primary_key=True)
    name = Column(TEXT, nullable=False)
    url = Column(TEXT, nullable=False)
    summary = Column(TEXT, nullable=True)
    birthdate = Column(DATETIME, nullable=True)
    deathdate = Column(DATETIME, nullable=True)
    cause_of_death = Column(TEXT, nullable=True)