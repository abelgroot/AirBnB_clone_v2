#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage
from sqlalchemy import Column, String

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', back_populates='states', cascade="all, delete")

    @property
    def cities(self):
      from models.city import City
      all_cities = storage.all()
      return [city for city in all_cities.values() if city.state_id == self.id]
    
    def __str__(self):
        """String representation of the State instance"""
        dict_repr =  self.__dict__.copy()
        dict_repr.pop("__class__", None)  # Remove the `__class__` key
        dict_repr.pop("_sa_instance_state", None)  # Remove the `_sa_instance_state` key
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,dict_repr)

