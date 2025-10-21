# review.py
from sqlalchemy.orm import validates
from config import db
from datetime import datetime 

class Review(db.Model):
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

    def __repr__(self):
        return f"<Review {self.id}: {self.content[:20]}... ({self.rating}/5)>"

    # ------------------ SERIALIZATION MANUELLE ------------------
    def to_dict(self):
        """
        Sérialise la critique, en utilisant les versions 'lite' des objets liés 
        (FoodUser et Restaurant) pour éviter les boucles de référence.
        """
        # Sérialise les données de base de la critique
        data = {
            "id": self.id,
            "content": self.content,
            "rating": self.rating,
            # Conversion de la date au format ISO pour JSON
            "review_date": self.review_date.isoformat() if self.review_date else None, 
            "food_user_id": self.food_user_id,
            "restaurant_id": self.restaurant_id
        }
        
        # Ajout de l'utilisateur (FoodUser) en version légère
        if self.food_user:
            data['food_user'] = self.food_user.food_user_lite_dict()
            
        # Ajout du restaurant en version légère
        if self.restaurant:
            data['restaurant'] = self.restaurant.restaurant_lite_dict()
            
        return data

    # ------------------ VALIDATIONS ------------------
    @validates("content")
    def validate_content(self, _, content):
        if not isinstance(content, str):
            raise TypeError("Le contenu doit être une chaîne de caractères")
        if not content.strip():
            raise ValueError("Le contenu ne doit pas être vide")
        return content

    @validates("rating")
    def validate_rating(self, key, rating):
        if rating is None:
            return None 
        if not isinstance(rating, (int, float)):
            raise TypeError("La note doit être un nombre")
        if rating < 0 or rating > 5:
            raise ValueError("La note doit être comprise entre 0 et 5")
        return rating
