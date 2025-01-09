#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    # Define the relationship with City
    cities = relationship('City', back_populates='state', cascade="all, delete")

    def __str__(self):
        """
        Returns a string representation of the State object, excluding
        SQLAlchemy internal state if present.
        """
        dict_copy = self.__dict__.copy()
        dict_copy.pop('_sa_instance_state', None)
        return f"[State] ({self.id}) {dict_copy}"
