from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel
from models.city import City


class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if models.storage_type == "db":
            self.cities = relationship(
                "City", back_populates="states", cascade="all, delete"
            )

    @property
    def cities(self):
        """getter attribute in case of file storage used."""
        if models.storage_type != "db":
            all_cities = models.storage.all(City)
            return [city for city in all_cities.values() if city.state_id == self.id]
        return []

