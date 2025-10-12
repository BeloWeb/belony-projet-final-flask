# dish.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class Dish(db.Model, SerializerMixin):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float)

    # Relationships
    menu_dishes = db.relationship('MenuDish', back_populates='dish')

    # Validations
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Dish name is required')
        if len(name) < 2:
            raise ValueError('Dish name must be at least 2 characters')
        return name

    @validates('description')
    def validate_description(self, key, description):
        # Add any specific validation rules for description here if needed
        return description

    @validates('price')
    def validate_price(self, key, price):
        if not isinstance(price, (int, float)):
            raise ValueError('Price must be a number')
        if price < 0:
            raise ValueError('Price cannot be negative')
        return price
