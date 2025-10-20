# menu.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
# L'importation de MenuDish est correcte si MenuDish est défini séparément
from menu_dish import MenuDish 

class Menu(db.Model, SerializerMixin):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    
    # Relationships
    restaurant = db.relationship('Restaurant', back_populates='menus')
    # Ajout de 'cascade' pour garantir la suppression des liens MenuDish lors de la suppression d'un Menu
    menu_dishes = db.relationship('MenuDish', back_populates='menu', cascade='all, delete-orphan') 
    
    # Association Proxy
    dishes = association_proxy('menu_dishes', 'dish')

    # serialization
    # CORRECTION : La règle "-menu_dishes." était incomplète. 
    # Nous la remplaçons par "-menu_dishes.menu" et ajoutons "dishes".
    serialize_only = (
        "id", 
        "name", 
        "restaurant_id", 
        # Relation avec le Restaurant (pour éviter la boucle)
        "restaurant", 
        "-restaurant.menus", 
        # Relation avec la table d'association (pour éviter la boucle)
        "menu_dishes", 
        "-menu_dishes.menu", 
        # Le proxy d'association qui contient les objets Dish réels
        "dishes"            
    )
    
    def __repr__(self):
        return f"<Menu {self.id}: {self.name}>"

    # validation
    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Le nom doit être une chaîne de caractères")
        # Utilisation de .strip() pour gérer les espaces blancs
        elif len(name.strip()) < 1: 
            raise ValueError("Le nom doit contenir au moins 1 caractère")
        return name

    @validates('restaurant_id')
    def validate_restaurant_id(self, key, restaurant_id):
        if not isinstance(restaurant_id, int):
            raise TypeError("L'ID du restaurant doit être un entier")
        elif restaurant_id <= 0:
            raise ValueError("ID de restaurant invalide")
        return restaurant_id