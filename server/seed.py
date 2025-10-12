import requests
from flask import Flask
from faker import Faker
from favorite import Favorite
from random import randint, choice
from datetime import datetime
from config import db
from restaurant import Restaurant
from menu import Menu
from dish import Dish
from menu_dish import MenuDish
from food_user import FoodUser
from review import Review
from random import sample 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Ensure this matches your actual database URI
db.init_app(app)

YELP_API_KEY = "nS0hSkt6MykfzvtTOX0nD8MexHqE5NYlAlaZUj6_r9_Uz6E-XTAypJc_N10lkzWj1wb2ZJ3QTsQH-x1u8SYFpxvzwpKGo2H01US8j-s-7_Bg_Y-OdhmyHWKKLAVzZXYx"  # Replace with your actual Yelp API key

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
        new_favorite = Favorite(food_user_id=food_user_id, restaurant_id=restaurant_id)
        db.session.add(new_favorite)
        db.session.commit()
        print(f"Added favorite: FoodUser {food_user_id} -> Restaurant {restaurant_id}")
    except Exception as e:
        print(f"Failed to add favorite: {e}")
        db.session.rollback()

def seed_database():
    fake = Faker()
    try:
        # Seed restaurants from Yelp data
        yelp_data = get_yelp_data()
        for data in yelp_data:  
            name = data.get('name')
            rating = data.get('rating')
            image_url = data.get('image_url')
            phone_number = data.get('phone')

            restaurant = Restaurant(name=name, rating=rating, image_url=image_url, phone_number=phone_number)
            db.session.add(restaurant)

        db.session.commit()

        

        # Sample Korean dishes
        sample_dishes = [
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
        for dish_data in sample_dishes:
            dish = Dish(name=dish_data['name'], description=dish_data['description'], price=dish_data['price'])
            db.session.add(dish)

        db.session.commit()

        # Create menus and assign dishes to restaurants
        dishes = Dish.query.all()
        restaurants = Restaurant.query.all()

        for restaurant in restaurants:
            # Create lunch and dinner menus for each restaurant
            lunch_menu = Menu(name="Lunch Menu", restaurant_id=restaurant.id)
            dinner_menu = Menu(name="Dinner Menu", restaurant_id=restaurant.id)
            db.session.add(lunch_menu)
            db.session.add(dinner_menu)

            # Randomly assign a subset of dishes to each menu
            lunch_dishes = sample(dishes, 25)  # Select 5 dishes for lunch
            dinner_dishes = sample(dishes, 25)  # Select 5 different dishes for dinner

            # Associate dishes with lunch menu
            for dish in lunch_dishes:
                menu_dish = MenuDish(menu=lunch_menu, dish=dish)
                db.session.add(menu_dish)

            # Associate dishes with dinner menu
            for dish in dinner_dishes:
                menu_dish = MenuDish(menu=dinner_menu, dish=dish)
                db.session.add(menu_dish)

                # Seed fake users
        for _ in range(20):  # Adjust number as needed
            food_user = FoodUser(
                username=fake.user_name(),
                email=fake.email(),
                _password_hash=fake.password()  # In reality, hash this password
            )
            db.session.add(food_user)

        db.session.commit()
        
        # Seed favorites
        food_users = FoodUser.query.all()
        restaurants = Restaurant.query.all()

        for food_user in food_users:
            favorite_restaurants = sample(restaurants, 10)  # Select 2 random restaurants
            for restaurant in favorite_restaurants:
                add_favorite(food_user.id, restaurant.id)



        # Seed fake reviews
        food_users = FoodUser.query.all()
        for restaurant in restaurants:
            for _ in range(15):  # Adjust number as needed
                review = Review(
                    content=fake.text(),
                    rating=randint(1, 5),
                    review_date=datetime.utcnow(),
                    food_user_id=choice(food_users).id,
                    restaurant_id=restaurant.id
                )
                db.session.add(review)

        db.session.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")
        seed_database()
