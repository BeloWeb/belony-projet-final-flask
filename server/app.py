from flask import jsonify, request, session, make_response
from flask_restful import Resource

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


# La configuration OAuth est conservée mais simplifiée pour le besoin du client.

class FoodUsers(Resource):
    def get(self):
        try:
            # ✅ Changement 1: Utilisation de la méthode to_dict() par défaut, 
            # qui est rapide et n'inclut pas les relations complètes.
            food_users = [food_user.to_dict() for food_user in FoodUser.query.all()]
            return food_users, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.json
            password = data.get('password')

            if not password:
                return {'message': 'Le mot de passe est requis pour l\'inscription'}, 400

            new_food_user = FoodUser(
                username = data.get('username'), 
                email = data['email']
            )
            new_food_user.password_hash = password 
            
            db.session.add(new_food_user)
            db.session.commit()
            
            session["food_user_id"] = new_food_user.id 
            # ✅ Changement 2: to_dict() sans argument.
            return new_food_user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

api.add_resource(FoodUsers, "/food_users")

class FoodUsersById(Resource):
    def get(self, id):
        food_user = db.session.get(FoodUser, id) 
        if not food_user:
            return {'message': f"FoodUser {id} non trouvé"}, 404

        # ✅ Changement 3: Utilisation de la méthode to_dict() complète du modèle FoodUser.
        # Cette méthode est censée sérialiser toutes les relations (reviews, favorites).
        # Nous supprimons l'argument `rules`.
        return food_user.to_dict(), 200

    def patch(self, id):
        food_user = db.session.get(FoodUser, id) 
        if not food_user:
            return {'message': f"FoodUser {id} non trouvé"}, 404

        try:
            data = request.json
            
            if 'username' in data:
                food_user.username = data['username']
            if 'email' in data:
                food_user.email = data['email'] 
                
            if 'newPassword' in data and 'currentPassword' in data:
                if not food_user._password_hash or not food_user.authenticate(data['currentPassword']):
                    return {'message': 'Le mot de passe actuel est incorrect'}, 400
                
                food_user.password_hash = data['newPassword'] 

            db.session.commit()
            # ✅ Changement 4: to_dict() sans argument.
            return food_user.to_dict(), 200 
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    def delete(self, id):
        food_user = db.session.get(FoodUser, id)
        if not food_user:
            return {'message': f"FoodUser {id} non trouvé"}, 404
            
        try:
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
        query = Review.query
        if restaurant_id:
            query = query.filter_by(restaurant_id=restaurant_id)
            
        # ✅ Changement 5: to_dict() sans argument. La sérialisation dans le modèle Review
        # inclut déjà le FoodUser et le Restaurant en version Lite.
        reviews = [review.to_dict() for review in query.all()]
        return reviews, 200

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
            # ❌ Changement 6: Remplacement de `only` par la méthode `restaurant_lite_dict()`.
            # Nous utilisons la version Lite pour les listes.
            restaurants = [restaurant.restaurant_lite_dict() for restaurant in Restaurant.query.all()]
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
            
        # ✅ Changement 7: to_dict() sans argument. La sérialisation complète inclut les menus, 
        # les critiques et les favoris.
        restaurant_dict = restaurant.to_dict() 
        
        # Logique pour formater 'favorited_by' (maintenue)
        if 'favorites' in restaurant_dict:
            # On assume que la sérialisation de Favorite inclut bien food_user en mode lite
            restaurant_dict['favorited_by'] = [fav.get('food_user', {}).get('username') 
                                               for fav in restaurant_dict['favorites'] 
                                               if fav.get('food_user')]
            del restaurant_dict['favorites']
            
        return restaurant_dict, 200

api.add_resource(RestaurantsById, "/restaurants/<int:id>")

@app.route('/menus')
def get_menus():
    restaurant_id = request.args.get('restaurant_id')
    query = Menu.query
    if restaurant_id:
        query = query.filter_by(restaurant_id=restaurant_id)
        
    # ✅ Changement 8: to_dict() sans argument.
    menus = [menu.to_dict() for menu in query.all()]
    return jsonify(menus)


class Favorites(Resource):
    def post(self):
        user_id = session.get('food_user_id')
        if not user_id:
            return {'error': 'Utilisateur non connecté'}, 401

        restaurant_id = request.json.get('restaurant_id')

        favorite = Favorite.query.filter_by(food_user_id=user_id, restaurant_id=restaurant_id).first()
        if favorite:
            return {'message': 'Ce restaurant est déjà dans vos favoris !'}, 400

        try:
            new_fav = Favorite(food_user_id=user_id, restaurant_id=restaurant_id)
            db.session.add(new_fav)
            db.session.commit()
            # ✅ Changement 9: to_dict() sans argument.
            return new_fav.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400
        
api.add_resource(Favorites, "/favorites")


class FavoritesById(Resource):
    def delete(self, id):
        restaurant_id = id
        
        user_id = session.get('food_user_id')
        if not user_id:
            return {'error': 'Utilisateur non connecté'}, 401
            
        try:
            favorite = Favorite.query.filter_by(food_user_id=user_id, restaurant_id=restaurant_id).first()

            if favorite:
                db.session.delete(favorite)
                db.session.commit()
                return {}, 204 
            else:
                return {'message': f'Le restaurant {restaurant_id} n\'est pas dans les favoris de l\'utilisateur {user_id}'}, 404

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400
            
api.add_resource(FavoritesById, "/favorites/<int:id>")

class Dishes(Resource):
    def get(self):
        try:
            # ✅ Changement 10: to_dict() sans argument.
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
            # ✅ Changement 11: to_dict() sans argument.
            return new_dish.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

api.add_resource(Dishes, "/dishes")

class Login(Resource): 
    def post(self): 
        try:
            data = request.json
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
                # ✅ Changement 12: to_dict() sans argument.
                return user.to_dict(), 200
            else:
                return {'message': 'Identifiants Invalides'}, 403
        except Exception as e:
            return {'message': str(e)}, 400

api.add_resource(Login, '/login')

class Logout(Resource):
    def delete(self): 
        session.pop('food_user_id', None)
        return {}, 204 

api.add_resource(Logout, '/logout')

class CheckSession(Resource): 
    def get(self): 
        if user := db.session.get(FoodUser, session.get("food_user_id")):
            # ❌ Changement 13: Utilisation de food_user_lite_dict() (plus simple) ou 
            # to_dict() par défaut sans les relations lourdes.
            # to_dict() dans FoodUser exclut déjà le hash et le email par défaut.
            return user.to_dict(), 200
        return {"message": "Non Autorisé"}, 401 

api.add_resource(CheckSession, '/check_session') 

# Google OAuth route (Personnalisée avec un token envoyé par le client)
@app.route('/login/google', methods=["POST"])
def google_login():
    data = request.json 
    access_token = data.get('access_token')
    
    if not access_token:
        return make_response({"message": "Token d'accès manquant"}, 400)

    # Récupération des informations utilisateur auprès de Google
    req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}",
        headers={"Content-Type": "application/json"}
    )
    
    if req.status_code != 200:
        return make_response({"message": "Échec de la vérification du token Google"}, 400)

    res = req.json()
    
    if res.get("verified_email"):
        email = res["email"]
        
        food_user = FoodUser.query.filter_by(email=email).first()
        
        if not food_user:
            food_user = FoodUser(
                username = res.get('name'), 
                email = email,
                google_id = res.get('id')
            )
            
            db.session.add(food_user)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response({'message': 'Échec de l\'inscription: ' + str(e)}, 400)

        session['food_user_id'] = food_user.id
        # ✅ Changement 14: to_dict() sans argument.
        return make_response(food_user.to_dict(), 200)

    return make_response({"message": "Email non vérifié par Google"}, 400)

# Gestionnaire d'erreurs
@app.errorhandler(404)
def handle_404(error):
    return make_response({'message': 'La ressource demandée n\'a pas été trouvée'}, 404)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
