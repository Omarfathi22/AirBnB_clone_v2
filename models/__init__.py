#!/usr/bin/python3
"""This script instantiates a storage object based on the environment variable HBNB_TYPE_STORAGE."""

import os

from models.engine.db_storage import DBStorage  # Importing the DBStorage class
from models.engine.file_storage import FileStorage  # Importing the FileStorage class

# Conditionally instantiate either DBStorage or FileStorage based on environment variable
storage = DBStorage() if os.getenv('HBNB_TYPE_STORAGE') == 'db' else FileStorage()

"""
A unique instance of either FileStorage or DBStorage, depending on the value of HBNB_TYPE_STORAGE.
"""

storage.reload()  # Reloads the storage, initializing the session and database engine
