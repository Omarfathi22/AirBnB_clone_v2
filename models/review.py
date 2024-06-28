#!/usr/bin/python3
""" Review module for the HBNB project """
import os
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = 'reviews'
    
    # Define place_id column, a string of maximum length 60 characters, foreign key to places.id
    place_id = Column(
        String(60), ForeignKey('places.id'), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define user_id column, a string of maximum length 60 characters, foreign key to users.id
    user_id = Column(
        String(60), ForeignKey('users.id'), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define text column, a string of maximum length 1024 characters, not nullable
    text = Column(
        String(1024), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
