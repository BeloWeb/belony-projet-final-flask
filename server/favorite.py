# favorite.py
from config import db
from datetime import datetime
# Note: Assurez-vous d'importer les autres modèles (FoodUser et Restaurant) 
# si vous les utilisez pour les méthodes lite_dict dans un fichier séparé.

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    food_user_id = db.Column(db.Integer, db.ForeignKey('food_users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    
    # Contrainte pour garantir qu'un utilisateur ne peut avoir qu'un seul favori par restaurant
    __table_args__ = (
        db.UniqueConstraint('food_user_id', 'restaurant_id', name='_user_restaurant_uc'),
    )
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Relationships
    # Ces relations nécessiteront la méthode 'lite_dict' sur les modèles FoodUser et Restaurant
    food_user = db.relationship('FoodUser', back_populates='favorites')
    restaurant = db.relationship('Restaurant', back_populates='favorites')

    def __repr__(self):
        return f"<Favorite {self.id}>"

    # ------------------ SERIALIZATION MANUELLE ------------------
    def to_dict(self):
        """
        Sérialise l'objet Favorite en un dictionnaire, 
        en utilisant des versions légères (lite_dict) des objets liés 
        pour éviter les boucles de référence infinies.
        """
        data = {
            "id": self.id, 
            "food_user_id": self.food_user_id, 
            "restaurant_id": self.restaurant_id, 
            # Convertit les objets datetime en format ISO 8601 (string)
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

        # Inclusion de l'objet Restaurant via une méthode légère
        if self.restaurant:
            # Assurez-vous que la méthode 'restaurant_lite_dict' existe sur le modèle Restaurant
            data['restaurant'] = self.restaurant.restaurant_lite_dict()
        
        # Inclusion de l'objet FoodUser via une méthode légère
        if self.food_user:
            # Assurez-vous que la méthode 'food_user_lite_dict' existe sur le modèle FoodUser
            data['food_user'] = self.food_user.food_user_lite_dict()
            
        return data
