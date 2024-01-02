#!/usr/bin/python3
"""Defines the database storage system for the application"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """
    This class represents a database storage system for the application

    Attributes:
        __engine: SQLAlchemy database engine
        __session: SQLAlchemy session

    Methods:
        __init__: Initializes a new DBStorage instance
        All(cls=None): Retrieves all objects of a given class
        new(obj): Adds an object to the current database session
        save(): Commits changes to the database session
        delete(obj=None): Deletes an object from the current database session
        reload(): Reinitializes the database session
        __engine = None
        __session = None
    """
    def __init__(self):
        """
        Initializes a new DBStorage instance and sets up the databaseconnection
        """
        db_user = getenv("HBNB_MYSQL_USER")
        db_password = getenv("HBNB_MYSQL_PWD")
        db_host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")
        db_env = getenv("HBNB_ENV")

        self.__engine = create_engine(f"mysql+mysqldb://{db_user}:"
                                      f"{db_password}@{db_host}/{db_name}", 
                                      pool_pre_ping=True)

        if db_env == "test":
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def all(self, cls=None):
        """
        Retrieves all objects of a given class or all objects from all classes
        Args:
            cls (class, optional): The class to filter objects by

        Returns:
            dict: A dictionary containing object instances
        """
        from models.base_model import Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        obj_dict = {}

        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query_result = self.__session.query(cls).all()
        else:
            classes = [User, State, City, Amenity, Place, Review]
            query_result = []
            for c in classes:
                query_result.extend(self.__session.query(c).all())

        for obj in query_result:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """
        Adds an object to the current database session

        Args:
            obj (Base): The object to add to the session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits changes to the database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session

        Args:
            obj (Base, optional): The object to delete from the session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reinitializes the database session and recreates database tables
        """
        from models.base_model import Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        call remove() method on the private session attribute (self.__session)
        tips or close() on the class Session
        """
        self.__session.close()
