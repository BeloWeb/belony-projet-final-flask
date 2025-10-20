# run.py

# Importe l'objet 'app' de votre fichier principal (où les ressources sont définies)
from app import app, db

# Il est crucial d'importer tous les modèles ici 
# pour que SQLAlchemy puisse les reconnaître et créer les tables.
from food_user import FoodUser
from restaurant import Restaurant
from menu import Menu
from dish import Dish
from menu_dish import MenuDish
from review import Review
from favorite import Favorite

def create_tables():
    """
    Crée les tables de la base de données si elles n'existent pas.
    Doit être exécuté dans le contexte de l'application (app.app_context()).
    """
    with app.app_context():
        # Cette ligne lit tous les modèles importés ci-dessus
        # pour générer le schéma de la base de données dans app.db.
        db.create_all() 
        print("Base de données et tables créées (app.db).")


if __name__ == '__main__':
    # Création des tables avant de lancer le serveur (peut être retiré après la première fois)
    create_tables()
    
    print("\n---------------------------------------------------------")
    print("API Food Review Démarrée !")
    print("Assurez-vous que .env contient une SECRET_KEY valide.")
    print("---------------------------------------------------------\n")
    
    # Lancement de l'application Flask
    app.run(port=5000, debug=True)

