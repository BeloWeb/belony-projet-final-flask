from sqlalchemy_serializer import SerializerMixin
# La validation n'est pas nécessaire ici car les FK garantissent l'intégrité
from config import db

class Favorite(db.Model, SerializerMixin):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    food_user_id = db.Column(db.Integer, db.ForeignKey('food_users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    
    # Ajout d'une contrainte d'unicité pour s'assurer qu'un utilisateur ne peut ajouter
    # un même restaurant à ses favoris qu'une seule fois.
    __table_args__ = (
        db.UniqueConstraint('food_user_id', 'restaurant_id', name='_user_restaurant_uc'),
    )
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Relationships
    food_user = db.relationship('FoodUser', back_populates='favorites')
    restaurant = db.relationship('Restaurant', back_populates='favorites')

    # Serialization
    # CORRECTION CRITIQUE : Utilisation de serialize_only pour inclure les objets liés 
    # tout en coupant les boucles de référence.
    serialize_only = (
        "id", 
        "food_user_id", 
        "restaurant_id", 
        "created_at", 
        "updated_at",
        
        # Inclure l'utilisateur, mais ne pas sérialiser sa liste complète de favoris
        "food_user", 
        "-food_user.favorites", 
        
        # Inclure le restaurant, mais ne pas sérialiser sa liste complète de favoris
        "restaurant", 
        "-restaurant.favorites"
    )

    def __repr__(self):
        return f"<Favorite {self.id}>"
