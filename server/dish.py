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
    # Ajout de cascade pour garantir la suppression des liens d'association
    menu_dishes = db.relationship('MenuDish', back_populates='dish', cascade='all, delete-orphan')

    # Serialization
    # CRITIQUE : Exclure la référence circulaire vers MenuDish
    serialize_only = ('id', 'name', 'description', 'price', '-menu_dishes')

    def __repr__(self):
        return f"<Dish {self.id}: {self.name}>"

    # Validations
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