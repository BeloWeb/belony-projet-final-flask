# Standard library imports
import os

# Remote library imports
# REMOVED: from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# UserMixin a été supprimé car vous n'utilisez pas Flask-Login
class FoodUser(db.Model): # REMOVED: SerializerMixin
    __tablename__ = 'food_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=True) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    _password_hash = db.Column(db.String(128), nullable=True) 
    
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # --- Relationships ---
    # Ces relations nécessitent que Review et Favorite aient leurs propres to_dict()
    reviews = db.relationship('Review', back_populates='food_user', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='food_user', cascade='all, delete-orphan')

    # --- Proxy ---
    # Accède directement aux objets Restaurant via la table Favorite
    restaurants = association_proxy("favorites", "restaurant")

    def __repr__(self):
        return f"<FoodUser {self.id}: {self.username}>"

    # ------------------ SERIALIZATION MANUELLE (LÉGÈRE) ------------------

    def food_user_lite_dict(self):
        """
        Version légère de la sérialisation, utilisée pour l'inclusion dans 
        les objets enfants (Review, Favorite) afin d'éviter la boucle infinie.
        Exclut les relations et les champs sensibles.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

    # ------------------ SERIALIZATION MANUELLE (COMPLÈTE) ------------------

    def to_dict(self):
        """
        Sérialisation complète du FoodUser pour l'API (e.g., /users/<id>).
        Exclut les informations sensibles (_password_hash).
        """
        # Commence par les attributs de base
        data = self.food_user_lite_dict()
        
        # Ajoute les dates et les infos OAuth
        data["google_id"] = self.google_id
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        data["updated_at"] = self.updated_at.isoformat() if self.updated_at else None
        
        # Inclusion des collections : Utilise to_dict() pour chaque objet lié.
        # Note : On utilise 'restaurants' (proxy) au lieu de 'favorites' pour simplifier la vue.
        # Chaque Restaurant doit avoir une méthode to_dict() ou restaurant_lite_dict().
        data["restaurants"] = [r.restaurant_lite_dict() for r in self.restaurants]

        # Reviews
        # Chaque Review doit avoir une méthode to_dict().
        data["reviews"] = [review.to_dict() for review in self.reviews]

        # Les favoris complets peuvent être inclus si nécessaire, mais souvent 'restaurants' suffit
        # data["favorites"] = [favorite.to_dict() for favorite in self.favorites]

        return data

    # ------------------ VALIDATIONS ET SÉCURITÉ (Inchangées) ------------------

    @validates("username")
    def validate_username(self, _, username):
        if username is None:
            return None 
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        elif len(username) < 1:
            raise ValueError("Username must be at least 1 character")
        return username

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes are super secret!")

    @password_hash.setter
    def password_hash(self, new_password):
        if new_password:
            self._password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        else:
            self._password_hash = None

    def authenticate(self, password_to_check):
        if not self._password_hash:
            return False
        return bcrypt.check_password_hash(self._password_hash, password_to_check)
