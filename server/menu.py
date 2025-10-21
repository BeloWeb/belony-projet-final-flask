# menu.py
# REMOVED: from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
# L'importation de MenuDish est correcte si MenuDish est défini séparément
# Si MenuDish n'est pas importé ici, assurez-vous qu'il l'est dans app.py
# ou que la relation est définie en utilisant une chaîne de caractères ('MenuDish').
# from menu_dish import MenuDish 

class Menu(db.Model):
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
    
    def __repr__(self):
        return f"<Menu {self.id}: {self.name}>"

    # ------------------ SERIALIZATION MANUELLE (LÉGÈRE) ------------------

    def menu_lite_dict(self):
        """
        Version légère de la sérialisation, utilisée pour l'inclusion 
        dans les objets parents si nécessaire.
        """
        return {
            "id": self.id,
            "name": self.name,
            "restaurant_id": self.restaurant_id,
        }

    # ------------------ SERIALIZATION MANUELLE (COMPLÈTE) ------------------

    def to_dict(self):
        """
        Sérialisation complète du menu, incluant les plats associés.
        """
        data = self.menu_lite_dict()
        
        # Inclure le restaurant parent (version légère)
        if self.restaurant:
            # Assurez-vous que la méthode 'restaurant_lite_dict' existe sur le modèle Restaurant
            data["restaurant"] = self.restaurant.restaurant_lite_dict()
            
        # Inclure les plats via le proxy (chaque Dish doit avoir une méthode to_dict())
        # Note : Si vous voulez le prix ou d'autres attributs de la table MenuDish, 
        # vous devriez sérialiser menu_dishes au lieu de dishes.
        data["dishes"] = [dish.to_dict() for dish in self.dishes]

        # Inclure la table d'association pour les détails (optionnel mais souvent utile)
        # data["menu_dishes"] = [md.to_dict() for md in self.menu_dishes]

        return data

    # ------------------ VALIDATIONS (Inchangées) ------------------

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
