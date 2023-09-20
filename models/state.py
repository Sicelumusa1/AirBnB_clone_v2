#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    #  For DBStorage
    if type(storage) == 'DBStorage':
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")

    #  For FileStorage
    @property
    def cities(self):
        from models import storage
        city_list = []
        for city in storage.all("City").values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
