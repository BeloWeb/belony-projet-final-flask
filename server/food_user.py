# user.py
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

class FoodUser(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'food_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=True)  # Made nullable for OAuth users
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=True)  # Nullable for OAuth users
    google_id = db.Column(db.String(100), unique=True, nullable=True)  # Google OAuth ID
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Relationships
    reviews = db.relationship('Review', back_populates='food_user', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='food_user', cascade='all, delete-orphan')

    # Serialize only specific fields
    serialize_only = ("id", "username", "email", "reviews", "-reviews.food_user", "favorites", "-favorites.user" )

    restaurants = association_proxy("favorites", "restaurant")

    def __repr__(self):
        return f"<FoodUser {self.id}: {self.username}>"


    _password_hash = db.Column(db.String(128))

    @validates("username")
    def validate_username(self, _, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        elif len(username) < 1:
            raise ValueError("Username must be at least 1 characters")
        return username

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes are super secret!")

    @password_hash.setter
    def password_hash(self, new_password):
        self._password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

    def authenticate(self, password_to_check):
        return bcrypt.check_password_hash(self._password_hash, password_to_check)
