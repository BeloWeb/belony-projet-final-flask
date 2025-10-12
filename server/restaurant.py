from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

from config import db


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float)
    image_url = db.Column(db.String)
    phone_number = db.Column(db.String)
    address = db.Column(db.String)

    # Relationships
    reviews = db.relationship('Review', back_populates='restaurant', cascade='all, delete-orphan')
    menus = db.relationship('Menu', back_populates='restaurant', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='restaurant')

    # Serialization
    serialize_only = ("id", "name", "rating", "image_url", "phone_number", "reviews","-reviews.restaurant", "menus","-menus.restaurant", "favorites","-favorites.restaurant","address")

    food_users = association_proxy("favorites", "food_user")

    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}>"

    # Validations
    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        elif len(name) < 1:
            raise ValueError("Name must be at least 1 character")
        return name

    @validates("rating")
    def validate_rating(self, _, rating):
        if rating is not None and (rating < 0 or rating > 5):
            raise ValueError('Rating must be between 0 and 5')
        return rating

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
    # Add phone number validation logic
        return phone_number

    @validates("image_url")
    def validate_image_url(self, key, image_url):
    # Add image URL validation logic
        return image_url

