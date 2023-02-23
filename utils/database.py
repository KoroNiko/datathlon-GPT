from sqlalchemy import BigInteger, CheckConstraint, Column, Date, DateTime, Float, ForeignKey, Index, Integer, \
    String, Table, Time, text, select, JSON

from sqlalchemy.dialects.mysql import TEXT, JSON, DATE, SMALLINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
# metadata = Base.metadata

class Colors(Base):
    __tablename__ = 'Colors'
    
    id = Column(INTEGER, primary_key=True)
    cluster_counts = Column(TEXT, nullable=False)
    rgb_colors = Column(TEXT, nullable=False)


class Category(Base):
    __tablename__ = 'Category'
    
    id = Column(INTEGER, primary_key=True)
    name = Column(TEXT, nullable=False)
    

class Subcategory(Base):
    __tablename__ = 'Subcategory'
    
    id = Column(INTEGER, primary_key=True)
    
    category_id = Column(ForeignKey('Category.id'), nullable=False)
    color_id = Column(ForeignKey('Colors.id'), nullable=False)
    
    name = Column(TEXT, nullable=False)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    picture_url = Column(TEXT, nullable=True)
    caption = Column(TEXT, nullable=True)
    
    category = relationship('Category')
    color = relationship('Colors')

class Artwork(Base):
    __tablename__ = 'Artwork'
    
    id = Column(INTEGER, primary_key=True)
    
    subcategory_id = Column(ForeignKey('Subcategory.id'), nullable=False)
    color_id = Column(ForeignKey('Colors.id'), nullable=False)
    
    name = Column(TEXT, nullable=False)
    url = Column(TEXT, nullable=False)
    year = Column(SMALLINT, nullable=True)
    summary = Column(TEXT, nullable=True)
    location = Column(TEXT, nullable=True)
    
    subcategory = relationship('Subcategory')
    colors = relationship('Colors')
    

class Events(Base):
    __tablename__ = 'Events'
    
    id = Column(INTEGER, primary_key=True)
    
    name = Column(TEXT, nullable=False)
    start_date = Column(SMALLINT, nullable=False)
    end_date = Column(SMALLINT, nullable=False)
    description = Column(TEXT, nullable=True)