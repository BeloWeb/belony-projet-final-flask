# menu_dish.py
# REMOVED: from sqlalchemy_serializer import SerializerMixin
from config import db

class MenuDish(db.Model):
    __tablename__ = 'menu_dishes'

    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    
    # Contrainte pour garantir qu'un plat n'est pas ajouté deux fois au même menu
    __table_args__ = (
        db.UniqueConstraint('dish_id', 'menu_id', name='_dish_menu_uc'),
    )

    # Relationships
    dish = db.relationship('Dish', back_populates='menu_dishes')
    menu = db.relationship('Menu', back_populates='menu_dishes')

    def __repr__(self):
        return f"<MenuDish {self.id}: Dish {self.dish_id} - Menu {self.menu_id}>"

    # ------------------ SERIALIZATION MANUELLE ------------------

    def to_dict(self):
        """
        Sérialise l'objet d'association MenuDish, incluant ses objets liés 
        (Menu et Dish) via leurs méthodes 'lite_dict' pour éviter les boucles.
        """
        data = {
            "id": self.id, 
            "dish_id": self.dish_id, 
            "menu_id": self.menu_id, 
            # Note: Si vous aviez d'autres champs ici (comme 'price' ou 'description_speciale'), 
            # ils seraient inclus ici.
        }

        # Inclusion du plat (Dish Lite)
        if self.dish:
            # Assurez-vous que la méthode 'dish_lite_dict' existe sur le modèle Dish
            data['dish'] = self.dish.dish_lite_dict()
        
        # Inclusion du menu (Menu Lite)
        if self.menu:
            # Assurez-vous que la méthode 'menu_lite_dict' existe sur le modèle Menu
            data['menu'] = self.menu.menu_lite_dict()
            
        return data
