#!/usr/bin/python3
"""model for db_storage"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base
from models.city import City
from models.state import State


class DBStorage:
    """DBStorage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Constructor"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{password}@{host}/{database}", pool_pre_ping=True
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all objects of a given class from the database session.
        If cls is None, query all objects from all classes.
        """
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        from models.user import User

        result = {}
        if cls:
            # Query all objects of the given class
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                result[key] = obj
        else:
            classes = [User, State, City, Amenity, Place, Review]
            for class_obj in classes:
                objects = self.__session.query(class_obj).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    result[key] = obj
        return result

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete the object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reload the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=True)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the session."""
        self.__session.close()
