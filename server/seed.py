# Standard library imports
import requests
from flask import Flask
from faker import Faker
from random import randint, choice, sample
from datetime import datetime
import os 
from dotenv import load_dotenv # Ajouté pour une bonne pratique de configuration

# Local imports
from config import db
from restaurant import Restaurant
from menu import Menu
from dish import Dish
from menu_dish import MenuDish
from food_user import FoodUser
from review import Review
from favorite import Favorite # ESSENTIEL : Importation du modèle Favorite

# Load environment variables (si nécessaire pour la clé secrète dans config.py)
load_dotenv() 

app = Flask(__name__)
# Utilisation de os.getenv pour la cohérence avec config.py
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
db.init_app(app)

# NOTE: La clé API ne devrait pas être dans le code source, mais dans .env.
# Pour le moment, nous laissons la clé ici, mais il est préférable d'utiliser os.environ.get('YELP_API_KEY')
YELP_API_KEY = "nS0hSkt6MykfzvtTOX0nD8MexHqE5NYlAlaZUj6_r9_Uz6E-XTAypJc_N10lkzWj1wb2ZJ3QTsQH-x1u8SYFpxvzwpKGo2H01US8j-s-7_Bg_Y-OdhmyHWKKLAVzZXYx"  # Remplacez par votre clé réelle

def get_yelp_data():
    params = {
        'location': 'Seattle',
        'categories': 'korean',
        'limit': 50  # Adjust based on your needs
    }

    headers = {
        'Authorization': f'Bearer {YELP_API_KEY}'
    }

    try:
        response = requests.get('https://api.yelp.com/v3/businesses/search', params=params, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors
        return response.json().get('businesses', [])
    except requests.RequestException as e:
        print(f"Error fetching data from Yelp API: {e}")
        return []
    
def add_favorite(food_user_id, restaurant_id):
    try:
        # Utilisation du modèle Favorite correctement importé
        new_favorite = Favorite(food_user_id=food_user_id, restaurant_id=restaurant_id)
        db.session.add(new_favorite)
        db.session.commit()
        # print(f"Added favorite: FoodUser {food_user_id} -> Restaurant {restaurant_id}") # Commenté pour des logs plus propres
    except Exception as e:
        # La plupart des erreurs ici seront des contraintes d'unicité (si elles sont définies)
        # print(f"Failed to add favorite: {e}") 
        db.session.rollback()

def seed_database():
    fake = Faker()
    try:
        # Nettoyage de la base de données avant le seeding
        print("Nettoyage des tables existantes...")
        db.drop_all()
        db.create_all()

        # Seed restaurants from Yelp data
        print("1. Ajout des restaurants à partir de l'API Yelp...")
        yelp_data = get_yelp_data()
        restaurants_list = []
        for data in yelp_data:  
            # Tentative de gérer les adresses multiples
            address_list = data.get('location', {}).get('display_address', [])
            address = ", ".join(address_list) if address_list else "Adresse non spécifiée"

            restaurant = Restaurant(
                name=data.get('name'), 
                rating=data.get('rating'), 
                image_url=data.get('image_url'), 
                phone_number=data.get('phone'),
                address=address # Ajout de l'adresse
            )
            db.session.add(restaurant)
            restaurants_list.append(restaurant)

        db.session.commit()
        print(f"   -> {len(restaurants_list)} restaurants ajoutés.")

        # Sample Korean dishes
        sample_dishes = [
            # La liste des plats est laissée telle quelle pour la brièveté du fichier
            {"name": "Bibimbap", "description": "Mixed rice with vegetables", "price": 12.99},
            {"name": "Kimchi Jjigae", "description": "Kimchi stew with tofu", "price": 13.99},
            {"name": "Bulgogi", "description": "Marinated beef BBQ", "price": 15.99},
            {"name": "Japchae", "description": "Stir-fried sweet potato noodles", "price": 14.99},
            {"name": "Tteokbokki", "description": "Spicy rice cakes", "price": 10.99},
            {"name": "Galbi", "description": "Grilled short ribs", "price": 16.99},
            {"name": "Sundubu-jjigae", "description": "Soft tofu stew", "price": 12.99},
            {"name": "Samgyeopsal", "description": "Grilled pork belly", "price": 14.99},
            {"name": "Haemul Pajeon", "description": "Seafood pancake", "price": 13.99},
            {"name": "Gimbap", "description": "Korean sushi rolls", "price": 9.99},
            {"name": "Dakgangjeong", "description": "Crispy fried chicken", "price": 11.99},
            {"name": "Mandu", "description": "Korean dumplings", "price": 10.99},
            {"name": "Naengmyeon", "description": "Cold buckwheat noodles", "price": 12.99},
            {"name": "Banchan", "description": "Small side dishes", "price": 5.99},
            {"name": "Bossam", "description": "Boiled pork wrap", "price": 15.99},
            {"name": "Jjajangmyeon", "description": "Black bean sauce noodles", "price": 13.99},
            {"name": "Soondae", "description": "Korean blood sausage", "price": 14.99},
            {"name": "Yukgaejang", "description": "Spicy beef soup", "price": 14.99},
            {"name": "Hobakjeon", "description": "Zucchini fritters", "price": 9.99},
            {"name": "Gamjatang", "description": "Pork bone soup", "price": 13.99},
            {"name": "Gujeolpan", "description": "Nine-sectioned plate with vegetables and meats", "price": 20.99},
            {"name": "Sinseollo", "description": "Meat and vegetables in rich broth", "price": 22.99},
            {"name": "Bulgogi", "description": "Thinly sliced beef marinated in soy sauce", "price": 15.99},
            {"name": "Dak galbi", "description": "Stir-fried marinated diced chicken in gochujang", "price": 14.99},
            {"name": "Samgyeopsal", "description": "Unseasoned grilled pork belly", "price": 14.99},
            {"name": "Makchang gui", "description": "Grilled pork large intestines", "price": 16.99},
            {"name": "Gobchang gui", "description": "Grilled small intestines of pork or ox", "price": 16.99},
            {"name": "Saengseon gui", "description": "Grilled fish", "price": 17.99},
            {"name": "Seokhwa gui", "description": "Grilled shellfish", "price": 18.99},
            {"name": "Deodeok gui", "description": "Grilled deodeok roots", "price": 15.99},
            {"name": "Beoseot gui", "description": "Grilled mushrooms", "price": 13.99},
            {"name": "Gim gui", "description": "Grilled dry laver", "price": 10.99},
            {"name": "Galbijjim", "description": "Braised marinated beef short rib with vegetables", "price": 18.99},
            {"name": "Andong jjimdak", "description": "Steamed chicken with vegetables and noodles", "price": 17.99},
            {"name": "Agujjim", "description": "Braised angler and vegetables", "price": 19.99},
            {"name": "Jeonbokjjim", "description": "Abalone marinated in soy sauce and rice wine", "price": 22.99},
            {"name": "Gyeran jjim", "description": "Steamed egg custard", "price": 9.99},
            {"name": "Oiseon", "description": "Steamed cucumber with beef and mushrooms", "price": 12.99},
            {"name": "Hobakjeon", "description": "Pan-fried Korean zucchini", "price": 11.99},
            {"name": "Dubujeon", "description": "Steamed tofu mixed with ground beef and vegetables", "price": 10.99},
            {"name": "Sannakji", "description": "Live octopus", "price": 23.99},
            {"name": "Yukhoe", "description": "Similar to beef tartare", "price": 18.99},
            {"name": "Sukhoe", "description": "Parboiled fish or squid", "price": 16.99},
            {"name": "Ganghoe", "description": "Rolls of scallions, carrots, and eggs", "price": 11.99},
            {"name": "Bossam", "description": "Steamed pork wrapped in a leaf vegetable", "price": 15.99},
            {"name": "Bbolsal", "description": "Pork cheeks marinated in salt and sesame oil", "price": 16.99},
            {"name": "Yukgaejang", "description": "Spicy soup with shredded beef", "price": 13.99},
            {"name": "Hoe", "description": "Raw seafood dish with gochujang or soy sauce", "price": 17.99},
            {"name": "Namul", "description": "Seasoned vegetables", "price": 9.99},
            {"name": "Saengchae", "description": "Shredded fresh vegetables with seasonings", "price": 10.99},
            {"name": "Oisaengchae", "description": "Cucumber dressed in pepper powder and seasonings", "price": 9.99},
            {"name": "Sukchae", "description": "Cooked vegetables", "price": 8.99},
            {"name": "Kongnamul", "description": "Soybean sprouts used in various dishes", "price": 7.99},
            {"name": "Japchae", "description": "Vermicelli noodles with stir-fried vegetables and beef", "price": 14.99},
            {"name": "Tteokguk", "description": "Rice cake soup", "price": 12.99},
            {"name": "Haejangguk", "description": "Soup with pork spine and vegetables", "price": 13.99},
            {"name": "Miyeok guk", "description": "Seaweed soup", "price": 11.99},
            {"name": "Manduguk", "description": "Dumpling soup", "price": 10.99},
            {"name": "Galbitang", "description": "Soup made from short rib", "price": 14.99},
            {"name": "Oritang", "description": "Stew with duck and vegetables", "price": 17.99},
            {"name": "Samgyetang", "description": "Soup with Cornish game hens and ginseng", "price": 18.99},
            {"name": "Seolleongtang", "description": "Beef bone stock simmered overnight", "price": 14.99},
            {"name": "Maeuntang", "description": "Hot and spicy fish soup", "price": 15.99},
            {"name": "Gamjatang", "description": "Spicy soup with pork spine and vegetables", "price": 13.99},
            {"name": "Daktoritang", "description": "Spicy chicken and potato stew", "price": 14.99},
            {"name": "Chueotang", "description": "Ground Loach soup", "price": 12.99},
            {"name": "Bosintang", "description": "Soup made primarily with dog meat", "price": 15.99},
            {"name": "Doenjang jjigae", "description": "Soybean paste soup", "price": 11.99},
            {"name": "Cheonggukjang jjigae", "description": "Soup made from thick soybean paste", "price": 10.99},
            {"name": "Gochujang jjigae", "description": "Chili pepper paste soup", "price": 11.99}
        ]


        # Seed dishes
        print("2. Ajout des plats...")
        for dish_data in sample_dishes:
            dish = Dish(name=dish_data['name'], description=dish_data['description'], price=dish_data['price'])
            db.session.add(dish)
        db.session.commit()
        print(f"   -> {len(sample_dishes)} plats ajoutés.")

        # Create menus and assign dishes to restaurants
        print("3. Création des menus et liens MenuDish...")
        dishes = Dish.query.all()
        restaurants = Restaurant.query.all()

        for restaurant in restaurants:
            # Create lunch and dinner menus for each restaurant
            lunch_menu = Menu(name="Lunch Menu", restaurant_id=restaurant.id)
            dinner_menu = Menu(name="Dinner Menu", restaurant_id=restaurant.id)
            db.session.add(lunch_menu)
            db.session.add(dinner_menu)

            # Randomly assign a subset of dishes to each menu (réduit la taille de l'échantillon pour éviter les erreurs)
            # Votre liste de plats est longue, mais nous allons échantillonner un plus petit nombre pour la clarté
            num_dishes = min(15, len(dishes))
            lunch_dishes = sample(dishes, num_dishes) 
            dinner_dishes = sample(dishes, num_dishes)

            # Associate dishes with lunch menu
            for dish in lunch_dishes:
                menu_dish = MenuDish(menu=lunch_menu, dish=dish)
                db.session.add(menu_dish)

            # Associate dishes with dinner menu
            for dish in dinner_dishes:
                menu_dish = MenuDish(menu=dinner_menu, dish=dish)
                db.session.add(menu_dish)

        db.session.commit()
        print("   -> Menus et associations MenuDish créés.")
        
        # Seed fake users
        print("4. Création des utilisateurs...")
        num_users = 20
        for _ in range(num_users): 
            # Note: _password_hash est utilisé ici, mais doit être haché dans le modèle FoodUser
            food_user = FoodUser(
                username=fake.user_name(),
                email=fake.email(),
                _password_hash=fake.password()  
            )
            db.session.add(food_user)

        db.session.commit()
        print(f"   -> {num_users} utilisateurs ajoutés.")
        
        # Seed favorites
        print("5. Ajout des favoris (Favorites)...")
        food_users = FoodUser.query.all()
        restaurants = Restaurant.query.all()

        for food_user in food_users:
            # Chaque utilisateur ajoute en favori 2 restaurants aléatoires
            num_favorites = min(2, len(restaurants))
            favorite_restaurants = sample(restaurants, num_favorites) 
            for restaurant in favorite_restaurants:
                add_favorite(food_user.id, restaurant.id)
        
        print("   -> Favoris créés.")

        # Seed fake reviews
        print("6. Ajout des critiques (Reviews)...")
        food_users = FoodUser.query.all()
        review_count = 0
        for restaurant in restaurants:
            for _ in range(5): # 5 critiques par restaurant
                review = Review(
                    content=fake.text(),
                    rating=randint(1, 5),
                    review_date=datetime.utcnow(),
                    food_user_id=choice(food_users).id,
                    restaurant_id=restaurant.id
                )
                db.session.add(review)
                review_count += 1

        db.session.commit()
        print(f"   -> {review_count} critiques ajoutées.")
        
        print("Base de données remplie avec succès (Seeded successfully)!")
    except Exception as e:
        print(f"ERREUR lors du remplissage de la base de données : {e}")
        db.session.rollback()

if __name__ == '__main__':
    # Le contexte de l'application est essentiel pour interagir avec SQLAlchemy
    with app.app_context():
        print("Début du remplissage de la base de données...")
        seed_database()
