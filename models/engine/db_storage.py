#!/usr/bin/python3
"""This module defines a class for managing database storage in the hbnb clone."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import urllib.parse

from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place, place_amenity
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in a SQL database."""
    __engine = None  # SQLAlchemy engine instance
    __session = None  # SQLAlchemy session instance

    def __init__(self):
        """Initialize the SQL database storage."""
        # Retrieve database connection details from environment variables
        user = os.getenv('HBNB_MYSQL_USER')
        pword = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        # Construct the database URL
        DATABASE_URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            user, pword, host, db_name
        )

        # Create the SQLAlchemy engine with connection pooling
        self.__engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )

        # Drop all tables if environment is 'test'
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a dictionary of all models currently in storage."""
        objects = dict()
        all_classes = (User, State, City, Amenity, Place, Review)

        # If no specific class is specified, query all registered classes
        if cls is None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            # Query objects of the specified class
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj

        return objects

    def delete(self, obj=None):
        """Remove an object from the storage database."""
        if obj is not None:
            # Delete the specified object from the database
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete(
                synchronize_session=False
            )

    def new(self, obj):
        """Add a new object to the storage database."""
        if obj is not None:
            try:
                # Add the object to the current session, flush, and refresh
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                # Rollback changes if an exception occurs
                self.__session.rollback()
                raise ex

    def save(self):
        """Commit the session changes to the database."""
        self.__session.commit()

    def reload(self):
        """Load the storage database."""
        # Create all tables defined in Base's metadata in the database
        Base.metadata.create_all(self.__engine)

        # Create a session factory bound to the engine with scoped session
        SessionFactory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """Close the storage engine."""
        # Close the current session
        self.__session.close()

