# menu.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
from menu_dish import MenuDish

class Menu(db.Model, SerializerMixin):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant = db.relationship('Restaurant', back_populates='menus')
    menu_dishes = db.relationship('MenuDish', back_populates='menu')
    dishes = association_proxy('menu_dishes', 'dish')

    # serialization
    serialize_only = ("id", "name", "restaurant_id", "restaurant", "-restaurant.menus", "menu_dishes", "-menu_dishes.")
    

    def __repr__(self):
        return f"<Menu {self.id}: {self.name}>"

    # validation
    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        elif len(name) < 1:
            raise ValueError("Name must be at least 1 character")
        return name

    @validates('restaurant_id')
    def validate_restaurant_id(self, key, restaurant_id):
        if restaurant_id <= 0:
            raise ValueError("Invalid restaurant ID")
        return restaurant_id


