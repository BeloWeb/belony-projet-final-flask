# menu_dish.py
from sqlalchemy_serializer import SerializerMixin
from config import db

class MenuDish(db.Model, SerializerMixin):
    __tablename__ = 'menu_dishes'

    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)

    # Relationships
    dish = db.relationship('Dish', back_populates='menu_dishes')
    menu = db.relationship('Menu', back_populates='menu_dishes')

    # Serialization
    serialize_only = ("id", "dish_id", "menu_id", "dish", "-dish.menu_dishes")

    def __repr__(self):
        return f"<MenuDish {self.id}: Dish {self.dish_id} - Menu {self.menu_id}>"
