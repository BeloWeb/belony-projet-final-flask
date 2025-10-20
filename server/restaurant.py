from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

# Assurez-vous que le fichier config.py est correctement importé
from config import db 


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float)
    image_url = db.Column(db.String)
    phone_number = db.Column(db.String)
    address = db.Column(db.String)

    # Relationships
    reviews = db.relationship('Review', back_populates='restaurant', cascade='all, delete-orphan')
    menus = db.relationship('Menu', back_populates='restaurant', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='restaurant')

    # Serialization
    # Note : Le format serialize_only est maintenu pour la compatibilité avec SQLAlchemy-Serializer
    serialize_only = (
        "id", "name", "rating", "image_url", "phone_number", 
        "reviews", "-reviews.restaurant", 
        "menus", "-menus.restaurant", 
        "favorites", "-favorites.restaurant", 
        "address"
    )

    food_users = association_proxy("favorites", "food_user")

    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}>"

    # ------------------ VALIDATIONS ------------------

    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Le nom doit être une chaîne de caractères")
        elif len(name.strip()) < 1:
            raise ValueError("Le nom doit contenir au moins 1 caractère")
        return name

    @validates("rating")
    def validate_rating(self, _, rating):
        # Permet None, mais si une valeur est fournie, elle doit être un nombre entre 0 et 5
        if rating is not None and (not isinstance(rating, (int, float)) or rating < 0 or rating > 5):
            raise ValueError('La note doit être un nombre entre 0 et 5')
        return rating

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if phone_number is None:
            return phone_number # Le champ est nullable

        if not isinstance(phone_number, str):
            raise TypeError("Le numéro de téléphone doit être une chaîne de caractères")

        # Autorise les chiffres, les espaces, les tirets, les parenthèses, et le signe plus
        valid_chars = set('0123456789 -()+.')
        
        if not all(c in valid_chars for c in phone_number):
             raise ValueError("Le numéro de téléphone contient des caractères non valides.")

        if not any(c.isdigit() for c in phone_number):
            raise ValueError("Le numéro de téléphone doit contenir au moins un chiffre")
            
        return phone_number

    @validates("image_url")
    def validate_image_url(self, key, image_url):
        if image_url is None:
            return image_url # Le champ est nullable

        if not isinstance(image_url, str):
            raise TypeError("L'URL de l'image doit être une chaîne de caractères")
        
        trimmed_url = image_url.strip()

        if len(trimmed_url) == 0:
            raise ValueError("L'URL de l'image ne peut pas être vide")
            
        # Doit commencer par un schéma http(s)
        if not (trimmed_url.startswith("http://") or trimmed_url.startswith("https://")):
            raise ValueError("L'URL de l'image doit être une adresse web valide (commencer par http:// ou https://)")

        return trimmed_url