#!/usr/bin/python3
"""State Module for HBNB project"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models import storage
from models.base_model import Base, BaseModel
from models.city import City


class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if models.storage_type == "db":
        cities = relationship("City", back_populates="states", cascade="all, delete")
    else:

        @property
        def cities(self):
            """getter attribute in case of file storage used."""
            all_cities = storage.all(City)
            return [city for city in all_cities.values() if city.state_id == self.id]

    def __str__(self):
        dict_copy = self.__dict__.copy()
        dict_copy.pop("_sa_instance_state", None)
        return f"[State] ({self.id}) {dict_copy}"

