#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            Getter method to return the list of City objects
            from storage linked to the current State
            """
            cities_list = []
            for city in storage.all("City").value():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
    else:
        @property
        def cities(self):
            """
            Getter method to return the list of City objects
            from storage linked to the current State
            """
            from models.city import City
            return storage.all(City).values()
