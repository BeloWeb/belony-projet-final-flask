from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

# Assurez-vous que le fichier config.py est correctement importé
from config import db 


# REMOVED: SerializerMixin
class Restaurant(db.Model):
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

    # Association Proxy
    food_users = association_proxy("favorites", "food_user")

    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}>"

    # ------------------ SERIALIZATION MANUELLE (LÉGÈRE) ------------------

    def restaurant_lite_dict(self):
        """
        Version légère de la sérialisation, utilisée pour l'inclusion 
        dans les objets enfants (Review, Favorite) afin d'éviter les boucles.
        """
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "image_url": self.image_url,
            "phone_number": self.phone_number,
            "address": self.address
        }

    # ------------------ SERIALIZATION MANUELLE (COMPLÈTE) ------------------

    def to_dict(self):
        """
        Sérialisation complète du restaurant, incluant les relations.
        Note: Les objets liés (reviews, menus, favorites) utilisent 
        leur propre méthode to_dict() pour sérialiser leur contenu.
        """
        # Commence par les attributs de base
        data = self.restaurant_lite_dict()
        
        # Inclusion des collections : Utilise la méthode to_dict() de chaque objet lié.
        # Vous devez vous assurer que Review.to_dict() et Favorite.to_dict() 
        # utilisent des versions légères du Restaurant pour ne pas boucler ici.
        
        # Reviews
        data["reviews"] = [review.to_dict() for review in self.reviews]
        
        # Menus
        data["menus"] = [menu.to_dict() for menu in self.menus]
        
        # Favorites (souvent on n'inclut que les ID ou un compte, mais ici on inclut la relation complète)
        data["favorites"] = [favorite.to_dict() for favorite in self.favorites]

        return data
        
    # ------------------ VALIDATIONS (Inchangées) ------------------

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
