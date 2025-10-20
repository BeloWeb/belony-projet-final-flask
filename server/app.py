from flask import jsonify, request, session, make_response
from flask_restful import Resource
# from authlib.integrations.flask_client import OAuth # Supprimé car non utilisé dans la logique actuelle
# from flask_login import LoginManager # Supprimé car vous utilisez la session Flask manuellement

from config import app, db, api, bcrypt

# Import your model files
from food_user import FoodUser
from restaurant import Restaurant
from menu import Menu
from dish import Dish
from menu_dish import MenuDish
from review import Review
from favorite import Favorite
import requests, json 


# Initialisation OAuth (Conservée pour la configuration Google, mais les composants Flask-Login sont supprimés)
# oauth = OAuth(app) # Commenté ou supprimé si non nécessaire pour la route /login/google


# OAuth Configuration for Google (ClientId mis en dur, à changer pour une variable d'environnement)
# Vous n'utilisez qu'une seule route personnalisée, pas le flow complet d'Authlib/OAuth.

# User loader for Flask-Login (Supprimé car vous utilisez la session Flask)
# @login_manager.user_loader
# def load_user(user_id):
#     return FoodUser.query.get(user_id)

class FoodUsers(Resource):
    def get(self):
        try:
            food_users = [food_user.to_dict() for food_user in FoodUser.query]
            return food_users, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.json # Simplifié
            password = data.get('password')

            if not password:
                 # Assurez-vous qu'un mot de passe est fourni pour l'inscription normale
                return {'message': 'Le mot de passe est requis pour l\'inscription'}, 400

            new_food_user = FoodUser(
                username = data.get('username'), 
                email = data['email']
            )
            # La propriété hybride dans votre modèle gère le hachage
            new_food_user.password_hash = password 
            
            db.session.add(new_food_user)
            db.session.commit()
            
            # Démarre la session utilisateur
            session["food_user_id"] = new_food_user.id 
            return new_food_user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

api.add_resource(FoodUsers, "/food_users")

class FoodUsersById(Resource):
    def get(self, id):
        # Utilisation de db.session.get() recommandé
        food_user = db.session.get(FoodUser, id) 
        if not food_user:
            return {'message': f"FoodUser {id} non trouvé"}, 404

        # Ajout de 'reviews' et 'restaurants' aux règles pour une vue complète
        return food_user.to_dict(rules=("reviews", "restaurants")), 200

    def patch(self, id):
        food_user = db.session.get(FoodUser, id) 
        if not food_user:
            return {'message': f"FoodUser {id} non trouvé"}, 404

        try:
            data = request.json
            
            # --- Mise à jour du nom d'utilisateur/email ---
            if 'username' in data:
                food_user.username = data['username']
            if 'email' in data:
                food_user.email = data['email'] 
                
            # --- Mise à jour du mot de passe ---
            if 'newPassword' in data and 'currentPassword' in data:
                # Vérifie si le mot de passe hashé existe avant d'authentifier
                if not food_user._password_hash or not food_user.authenticate(data['currentPassword']):
                    return {'message': 'Le mot de passe actuel est incorrect'}, 400
                
                # Le setter de votre modèle s'occupe du hachage
                food_user.password_hash = data['newPassword'] 

            db.session.commit()
            # Retourne les données utilisateur mises à jour
            return food_user.to_dict(), 200 
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    def delete(self, id):
        food_user = db.session.get(FoodUser, id)
        if not food_user:
            return {'message': f"FoodUser {id} non trouvé"}, 404
            
        try:
            # S'assurer que l'utilisateur déconnecte avant de supprimer
            if session.get('food_user_id') == food_user.id:
                 session.pop('food_user_id', None) 

            db.session.delete(food_user)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

api.add_resource(FoodUsersById, "/food_users/<int:id>")

class Reviews(Resource):
    def get(self):
        restaurant_id = request.args.get('restaurant_id')
        if restaurant_id:
            reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()
        else:
            reviews = Review.query.all()
        return [review.to_dict() for review in reviews], 200

    def post(self):
        data = request.json
        try:
            new_review = Review(
                content=data['content'],
                rating=data['rating'],
                restaurant_id=data['restaurant_id'],
                food_user_id=data['food_user_id']
            )
            db.session.add(new_review)
            db.session.commit()
            return new_review.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    # L'ID est maintenant correctement attendu dans l'URL
    def patch(self, id): 
        review = db.session.get(Review, id)
        if not review:
            return {'message': f"Review {id} non trouvé"}, 404

        try:
            data = request.json
            if 'content' in data:
                review.content = data['content']
            if 'rating' in data:
                review.rating = data['rating']
            
            db.session.commit()
            return review.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    # L'ID est maintenant correctement attendu dans l'URL
    def delete(self, id): 
        review = db.session.get(Review, id)
        if not review:
            return {'message': f"Review {id} non trouvé"}, 404

        try:
            db.session.delete(review)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

api.add_resource(Reviews, '/reviews', '/reviews/<int:id>')


class Restaurants(Resource):
    def get(self):
        try:
            # Simplifié pour la liste
            restaurants = [restaurant.to_dict(only=("id", "name", "rating", "image_url", "phone_number", "address")) for restaurant in Restaurant.query]
            return restaurants, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.json
            new_restaurant = Restaurant(
                name=data['name'],
                rating=data.get('rating'),
                image_url=data.get('image_url'),
                phone_number=data.get('phone_number'),
                address=data.get('address')
            )
            db.session.add(new_restaurant)
            db.session.commit()
            return new_restaurant.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

api.add_resource(Restaurants, "/restaurants")

class RestaurantsById(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
             return {'message': f"Restaurant {id} non trouvé"}, 404
             
        # Utilisation des règles de sérialisation par défaut du modèle pour inclure les menus et les critiques
        restaurant_dict = restaurant.to_dict() 
        
        # Logique pour formater 'favorited_by' (maintenue)
        if 'favorites' in restaurant_dict:
            # Assurez-vous que food_user est sérialisé pour obtenir l'username
            restaurant_dict['favorited_by'] = [fav.get('food_user', {}).get('username') 
                                                for fav in restaurant_dict['favorites'] 
                                                if fav.get('food_user')]
            del restaurant_dict['favorites']
            
        return restaurant_dict, 200

api.add_resource(RestaurantsById, "/restaurants/<int:id>")

@app.route('/menus')
def get_menus():
    restaurant_id = request.args.get('restaurant_id')
    if restaurant_id:
        menus = Menu.query.filter_by(restaurant_id=restaurant_id).all()
    else:
        menus = Menu.query.all()
        
    return jsonify([menu.to_dict() for menu in menus])


class Favorites(Resource):
    def post(self):
        # Vérification si un utilisateur est connecté
        user_id = session.get('food_user_id')
        if not user_id:
            return {'error': 'Utilisateur non connecté'}, 401

        restaurant_id = request.json.get('restaurant_id')

        # Vérification de l'existence du favori
        favorite = Favorite.query.filter_by(food_user_id=user_id, restaurant_id=restaurant_id).first()
        if favorite:
            return {'message': 'Ce restaurant est déjà dans vos favoris !'}, 400

        # Création du favori
        try:
            new_fav = Favorite(food_user_id=user_id, restaurant_id=restaurant_id)
            db.session.add(new_fav)
            db.session.commit()
            return new_fav.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400
        
api.add_resource(Favorites, "/favorites")


class FavoritesById(Resource):
    def delete(self, id):
        # L'ID est traité comme restaurant_id pour la suppression
        restaurant_id = id
        
        # Vérification de session
        user_id = session.get('food_user_id')
        if not user_id:
             return {'error': 'Utilisateur non connecté'}, 401
             
        try:
            # Trouve le favori spécifique pour l'utilisateur et le restaurant
            favorite = Favorite.query.filter_by(food_user_id=user_id, restaurant_id=restaurant_id).first()

            if favorite:
                db.session.delete(favorite)
                db.session.commit()
                # Retourne 204 No Content
                return {}, 204 
            else:
                return {'message': f'Le restaurant {restaurant_id} n\'est pas dans les favoris de l\'utilisateur {user_id}'}, 404

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400
            
    # La méthode PATCH est SUPPRIMÉE car elle était redondante et erronée 
    # (elle modifiait l'utilisateur au lieu du favori).
    # Les mises à jour de l'utilisateur se font via /food_users/<int:id>
        
api.add_resource(FavoritesById, "/favorites/<int:id>")

class Dishes(Resource):
    def get(self):
        try:
            dishes = [dish.to_dict() for dish in Dish.query.all()]
            return dishes, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.json
            new_dish = Dish(name=data['name'], description=data['description'], price=data['price'])
            db.session.add(new_dish)
            db.session.commit()
            return new_dish.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

api.add_resource(Dishes, "/dishes")

class Login(Resource): 
    def post(self): 
        try:
            data = request.json
            # Cherche par username ou email pour plus de flexibilité
            login_id = data.get('username_or_email') 
            password = data.get('password')
            
            if not login_id or not password:
                 return {'message': 'Nom d\'utilisateur/email et mot de passe requis'}, 403

            user = FoodUser.query.filter(
                 (FoodUser.username == login_id) | 
                 (FoodUser.email == login_id) 
            ).first()

            if user and user.authenticate(password):
                session['food_user_id'] = user.id
                return user.to_dict(), 200
            else:
                return {'message': 'Identifiants Invalides'}, 403
        except Exception as e:
            return {'message': str(e)}, 400

api.add_resource(Login, '/login')

class Logout(Resource):
    def delete(self): 
        # Si la session existe, la supprime.
        session.pop('food_user_id', None)
        return {}, 204 

api.add_resource(Logout, '/logout')

class CheckSession(Resource): 
    def get(self): 
        # Utilisation de l'opérateur walrus (:=) pour la vérification concise
        if user := db.session.get(FoodUser, session.get("food_user_id")):
            return user.to_dict(rules=("-email",)), 200
        return {"message": "Non Autorisé"}, 401 # Remplacé 403 par 401 (Non autorisé) plus précis

api.add_resource(CheckSession, '/check_session') 

# Google OAuth route (Personnalisée avec un token envoyé par le client)
@app.route('/login/google', methods=["POST"])
def google_login():
    data = request.json # Simplifié
    access_token = data.get('access_token')
    
    if not access_token:
        return make_response({"message": "Token d'accès manquant"}, 400)

    # Récupération des informations utilisateur auprès de Google
    req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}",
        headers={"Content-Type": "application/json"} # Type de contenu correct
    )
    
    if req.status_code != 200:
        return make_response({"message": "Échec de la vérification du token Google"}, 400)

    res = req.json()
    
    if res.get("verified_email"):
        email = res["email"]
        
        food_user = FoodUser.query.filter_by(email=email).first()
        
        if not food_user:
            # Création d'un nouvel utilisateur OAuth (SANS mot de passe)
            food_user = FoodUser(
                username = res.get('name'), 
                email = email,
                google_id = res.get('id') # Stocker l'ID Google si vous l'utilisez
            )
            # 🛑 IMPORTANT : Ne définissez PAS de mot de passe.
            # Le _password_hash dans le modèle reste None.
            
            db.session.add(food_user)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                # Gérer les erreurs de contrainte unique (email déjà utilisé)
                return make_response({'message': 'Échec de l\'inscription: ' + str(e)}, 400)

        # Démarre la session
        session['food_user_id'] = food_user.id
        return make_response(food_user.to_dict(), 200)

    return make_response({"message": "Email non vérifié par Google"}, 400)

# La route /authorize et /current_user sont supprimées car elles étaient redondantes ou brisées.


# Gestionnaire d'erreurs
@app.errorhandler(404)
def handle_404(error):
    # Utilisation de la méthode make_response pour uniformité
    return make_response({'message': 'La ressource demandée n\'a pas été trouvée'}, 404)


if __name__ == '__main__':
    # Le mode debug est dangereux en production
    app.run(port=5000, debug=True)