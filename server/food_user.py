# from flask_login import UserMixin  <-- Supprimé (inutilisé dans votre app)
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# UserMixin a été supprimé car vous n'utilisez pas Flask-Login
class FoodUser(db.Model, SerializerMixin):
    __tablename__ = 'food_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=True)  # OK: Nullable pour OAuth
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # CORRIGÉ: Définition unique de _password_hash
    _password_hash = db.Column(db.String(128), nullable=True) # OK: Nullable pour OAuth
    
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # --- Relationships ---
    reviews = db.relationship('Review', back_populates='food_user', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='food_user', cascade='all, delete-orphan')

    # --- Proxy ---
    # Accède directement aux objets Restaurant via la table Favorite
    restaurants = association_proxy("favorites", "restaurant")

    # --- Serialization Rules ---
    # AMÉLIORÉ: Utilisation de serialize_rules pour plus de flexibilité
    # - Exclut le mot de passe (sécurité)
    # - Exclut la relation 'favorites' (redondante avec le proxy 'restaurants')
    # - Inclut 'reviews' et 'restaurants' mais empêche les boucles infinies
    serialize_rules = (
        '-_password_hash',
        '-favorites', 
        'reviews', 
        '-reviews.food_user',
        'restaurants',
        '-restaurants.favorites', # Empêche la boucle retour vers 'favorites'
        '-restaurants.reviews',   # Empêche d'inclure les reviews des restaurants ici
    )

    def __repr__(self):
        return f"<FoodUser {self.id}: {self.username}>"

    # La 2ème définition de _password_hash (ligne 30) a été SUPPRIMÉE

    # CORRIGÉ: Le validateur autorise 'None' pour les utilisateurs OAuth
    @validates("username")
    def validate_username(self, _, username):
        if username is None:
            return None  # Autorise les utilisateurs OAuth sans username
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
        # Ne crypte pas si le mot de passe est 'None' (cas OAuth)
        if new_password:
            self._password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        else:
            self._password_hash = None

    def authenticate(self, password_to_check):
        # Gère le cas où un utilisateur OAuth n'a pas de mot de passe défini
        if not self._password_hash:
            return False
        return bcrypt.check_password_hash(self._password_hash, password_to_check)