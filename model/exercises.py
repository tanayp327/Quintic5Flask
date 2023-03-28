from sqlalchemy import Column, Integer, String
from __init__ import app, db

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    category = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
