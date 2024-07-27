#!/usr/bin/python3
"""This script instantiates a storage object based on the environment variable HBNB_TYPE_STORAGE."""

-> If the environmental variable 'HBNB_TYPE_STORAGE' is set to 'db',
   instantiates a database storage engine (DBStorage).
-> Otherwise, instantiates a file storage engine (FileStorage).
"""
from os import getenv

# Check if the environment variable for database storage is set
if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    # Import pymysql or mysqlclient here to handle MySQL connections
    import pymysql
    pymysql.install_as_MySQLdb()
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Reload storage configuration
storage.reload)
