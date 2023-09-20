#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv

#  Check the value of HBNB_TYPE_STORAGE environment variable
storage_type = getenv("HBNB_TYPE_STORAGE")

#  Depending on the storage type, import and create the appropriate
#  storage instance

if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

#  Reload the storage instance
storage.reload()
