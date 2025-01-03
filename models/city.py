#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey('states.id'),  nullable=False, )
    name = Column(String(128), nullable=False)
    state = relationship("State", backref="cities", cascade="all, delete")
    def __str__(self):
        """String representation of the State instance"""
        dict_repr =  self.__dict__.copy()
        dict_repr.pop("__class__", None)  # Remove the `__class__` key
        dict_repr.pop("_sa_instance_state", None)  # Remove the `_sa_instance_state` key
        dict_repr.pop("updated_at", None)  # Remove the `_sa_instance_state` key
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,dict_repr)
