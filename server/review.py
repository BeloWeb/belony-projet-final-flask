# review.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db
from datetime import datetime 
# food_user est importé, c'est bien, on suppose que Restaurant est disponible via config ou importé ailleurs

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)
    food_user_id = db.Column(db.Integer, db.ForeignKey('food_users.id'), nullable=False) 
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    # Relationships
    food_user = db.relationship('FoodUser', back_populates='reviews')
    restaurant = db.relationship('Restaurant', back_populates='reviews')

    # Serialization
    # CORRECTION : Ajout des relations et coupe des boucles de référence
    serialize_only = (
        "id", 
        "content", 
        "rating", 
        "review_date", 
        "food_user_id", 
        "restaurant_id",
        
        # Inclure l'utilisateur et le restaurant, mais couper la boucle
        "food_user", 
        "-food_user.reviews",
        "restaurant", 
        "-restaurant.reviews"
    )

    def __repr__(self):
        return f"<Review {self.id}: {self.content[:20]}... ({self.rating}/5)>"

    # ------------------ VALIDATIONS ------------------
    
    @validates("content")
    def validate_content(self, _, content):
        if not isinstance(content, str):
            raise TypeError("Le contenu doit être une chaîne de caractères")
        if not content.strip():
            # Utilisation de .strip() pour éviter les contenus composés uniquement d'espaces
            raise ValueError("Le contenu ne doit pas être vide")
        return content

    @validates("rating")
    def validate_rating(self, key, rating):
        if rating is None:
             # Si rating est nullable dans la DB et que vous voulez l'autoriser
             return None 
             
        if not isinstance(rating, (int, float)):
             raise TypeError("La note doit être un nombre")

        if rating < 0 or rating > 5:
            raise ValueError("La note doit être comprise entre 0 et 5")
            
        return rating