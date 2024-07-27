#!/usr/bin/python3
""" city module for hnb project """
import os
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

class City(BaseModel, Base):
    """ The city class, contains state id and names """
    __tablename__ = 'cities'
    
    # Define name column, a string of maximum length 128 characters, not nullable
    name = Column(
        String(128), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define state_id column, a string of maximum length 60 characters, foreign key to states.id, not nullable
    state_id = Column(
        String(60), ForeignKey('states.id'), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define places relationship, one-to-many relationship with Place model, cascade delete operations
    places = relationship(
        'Place',
        cascade='all, delete, delete-orphan',
        backref='cities'
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
