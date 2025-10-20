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
    # CORRECTION : Ajout de la règle pour couper la boucle Menu -> MenuDish -> Menu
    serialize_only = (
        "id", 
        "dish_id", 
        "menu_id", 
        "dish", 
        "-dish.menu_dishes", # Coupe la boucle Dish -> MenuDish -> Dish
        "menu",
        "-menu.menu_dishes"  # NOUVEAU : Coupe la boucle Menu -> MenuDish -> Menu
    )

    def __repr__(self):
        return f"<MenuDish {self.id}: Dish {self.dish_id} - Menu {self.menu_id}>"