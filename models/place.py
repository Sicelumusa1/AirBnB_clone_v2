#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table

from models.base_model import BaseModel, Base
from models import storage
from models.amenity import Amenity
from models.review import Review

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if type(storage) == 'DBStorage':
        reviews = relationship("Review", backref="place",
                cascade="all, delete-orphan, delete")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")

    # For FileStorage
    @property
    def reviews(self):
        """
        Getter attribute for reviews related to the Place.
        Returns a list of Review instances with matching place_id.
        """
        return [review for review in storage.all(Review).values() if review.place_id == self.id]

    @property
    def amenities(self):
        """ Returns list of amenity ids """
        return [storage.all(Amenity).get(amenity_id) for amenity_id 
                in self.amenity_ids if storage.all(Amenity).get(amenity_id)]

    @amenities.setter
    def amenities(self, obj=None):
        """ Appends amenity ids to the attribute """
        if type(value) == Amenity:
                self.amenity_ids.append(value.id)
