# dish.py
# REMOVED: from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float)

    # Relationships
    # Ajout de cascade pour garantir la suppression des liens d'association
    menu_dishes = db.relationship('MenuDish', back_populates='dish', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Dish {self.id}: {self.name}>"

    # ------------------ SERIALIZATION MANUELLE (LÉGÈRE) ------------------

    def dish_lite_dict(self):
        """
        Version légère de la sérialisation, utilisée pour l'inclusion 
        dans les objets d'association (MenuDish) afin d'éviter les boucles.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
        }
        
    # ------------------ SERIALIZATION MANUELLE (COMPLÈTE) ------------------

    def to_dict(self):
        """
        Sérialisation complète du plat, incluant ses liens d'association (MenuDish).
        """
        # Commence par la version légère
        data = self.dish_lite_dict()
        
        # Inclure la table d'association MenuDish
        # Chaque MenuDish doit avoir une méthode to_dict() pour être sérialisé
        data["menu_dishes"] = [md.to_dict() for md in self.menu_dishes]

        return data

    # ------------------ VALIDATIONS ------------------

    @validates('name')
    def validate_name(self, key, name):
        # Utilisation de .strip() pour une meilleure vérification des espaces
        stripped_name = name.strip()
        if not stripped_name:
            raise ValueError('Le nom du plat est requis')
        if len(stripped_name) < 2:
            raise ValueError('Le nom du plat doit contenir au moins 2 caractères')
        return stripped_name

    @validates('description')
    def validate_description(self, key, description):
        if description is None:
            return None
        if not isinstance(description, str):
            raise TypeError("La description doit être une chaîne de caractères")
        
        # Retourne la description nettoyée des espaces superflus
        return description.strip()

    @validates('price')
    def validate_price(self, key, price):
        if price is None:
            return None # Autorise None si la colonne DB le permet
            
        if not isinstance(price, (int, float)):
            raise ValueError('Le prix doit être un nombre')
        if price < 0:
            raise ValueError('Le prix ne peut pas être négatif')
            
        # Arrondit le prix à deux décimales pour l'uniformité
        return round(price, 2)
