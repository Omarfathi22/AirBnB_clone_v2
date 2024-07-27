#!/usr/bin/python3
"""This module defines a class User"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    
    # Define email column, which is a string of maximum length 128 characters
    email = Column(
        String(128), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define password column, also a string of maximum length 128 characters
    password = Column(
        String(128), nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define first_name column, a nullable string of maximum length 128 characters
    first_name = Column(
        String(128), nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define last_name column, a nullable string of maximum length 128 characters
    last_name = Column(
        String(128), nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    
    # Define relationship to places, cascading all operations (create, delete) and backref to user
    places = relationship(
        'Place',
        cascade="all, delete, delete-orphan",
        backref='user'
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    
    # Define relationship to reviews, cascading all operations (create, delete) and backref to user
    reviews = relationship(
        'Review',
        cascade="all, delete, delete-orphan",
        backref='user'
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None

