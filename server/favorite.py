# favorite.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class Favorite(db.Model, SerializerMixin):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    food_user_id = db.Column(db.Integer, db.ForeignKey('food_users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    # Relationships
    
    food_user = db.relationship('FoodUser', back_populates='favorites')
    restaurant = db.relationship('Restaurant', back_populates='favorites')

    serialize_rules = ("-food_user", "-restaurant", "-created_at", "-updated_at" )#"-food_user.favorites", "restaurant","-restaurant.favorites",

    def __repr__(self):
        return f"<Favorite {self.id}>"
 