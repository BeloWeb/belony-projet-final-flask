
from flask import jsonify, request, session, make_response
from flask_restful import Resource
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager

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


# Initialize OAuth and Flask-Login
oauth = OAuth(app)
login_manager = LoginManager(app)


# OAuth Configuration for Google
google = oauth.register(
    name='google',
    client_id='9656575814-i0rc5aehtlvhkv8fu23gnmgrtnspf5ps.apps.googleusercontent.com',
    # client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return FoodUser.query.get(user_id)

class FoodUsers(Resource):
    def get(self):
        try:
            food_users = [food_user.to_dict() for food_user in FoodUser.query]
            return food_users, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            new_food_user = FoodUser(username = data['username'], email = data['email'])
            new_food_user.password_hash = data.get('password')
            db.session.add(new_food_user)
            db.session.commit()
            session["food_user_id"]=new_food_user.id
            return new_food_user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

api.add_resource(FoodUsers, "/food_users")

class FoodUsersById(Resource):
    def get(self, id):
        food_user = FoodUser.query.get_or_404(id, description=f"FoodUser {id} not found")
        return food_user.to_dict(rules=("restaurants",)), 200

    def patch(self, id):
        food_user = FoodUser.query.get_or_404(id, description=f"FoodUser {id} not found")
        try:
            data = request.get_json()
            if 'username' in data:
                food_user.username = data['username']
            if 'email' in data:
                food_user.email = data['email'] 
            if 'newPassword' in data and 'currentPassword' in data:
                if not food_user.authenticate(data['currentPassword']):
                    return {'message': 'Current password is incorrect'}, 400
                food_user.password_hash = data['newPassword']

            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, id):
        food_user = FoodUser.query.get_or_404(id, description=f"FoodUser {id} not found")
        try:
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
        data = request.get_json()
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
        review = Review.query.get_or_404(id, description=f"Review {id} not found")
        try:
            data = request.get_json()
            if 'content' in data:
                review.content = data['content']
            if 'rating' in data:
                review.rating = data['rating']
            # Add other fields as necessary

            db.session.commit()
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

    def delete(self, id):
        review = Review.query.get_or_404(id, description=f"Review {id} not found")
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
            restaurants = [restaurant.to_dict(only=("id", "name", "rating", "image_url", "phone_number")) for restaurant in Restaurant.query]
            return restaurants, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            new_restaurant = Restaurant(
                name=data['name'],
                rating=data['rating'],
                image_url=data['image_url'],
                phone_number=data['phone_number'],
                address=data['address']
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
        restaurant = Restaurant.query.get_or_404(id, description=f"Restaurant {id} not found")
        restaurant = restaurant.to_dict(only=(
            "id", "name", "rating", "phone_number", "image_url", 
            "reviews.content", "reviews.rating", "reviews.review_date", "reviews.food_user_id",
            "favorites.food_user.username", "menus.restaurant_id", "menus.id", "menus.name", "reviews.id"
        ))
        restaurant['favorited_by'] = [fav['food_user']['username'] for fav in restaurant['favorites']]
        del restaurant['favorites']
        return restaurant, 200

api.add_resource(RestaurantsById, "/restaurants/<int:id>")

@app.route('/menus')
def get_menus():
    restaurant_id = request.args.get('restaurant_id')
    if restaurant_id:
        menus = Menu.query.filter_by(restaurant_id=restaurant_id).all()
        # Serialize and return menus along with dish details
    else:
        menus = Menu.query.all()
        # Serialize and return all menus
    return jsonify([menu.to_dict() for menu in menus])


class Favorites(Resource):
    def post(self):
        # Check if a user is logged in
        if 'food_user_id' not in session:
            return {'error': 'FoodUser not logged in'}, 401

        user_id = session['food_user_id']
        restaurant_id = request.json.get('restaurant_id')

        # Check if the user has already favorited this restaurant
        favorite = Favorite.query.filter_by(food_user_id=user_id, restaurant_id=restaurant_id).first()
        if favorite:
            return {'message': 'You already have this restaurant favorited!'}, 400

        # If not already favorited, create a new favorite record
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
        try:
            user_id = session['food_user_id']
            print(user_id)
            favorite = Favorite.query.filter_by(food_user_id=user_id, restaurant_id=id).first()

            if favorite:
                db.session.delete(favorite)
                db.session.commit()
                return {}, 201
            else:
                return {'message': f'FoodUser {id} does not have restaurant {id}'}, 400

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400
    def patch(self, id):
        food_user = FoodUser.query.get_or_404(id, description=f"FoodUser {id} not found")
        data = request.get_json()
        try:
            # Verify current password if attempting to change password
            if 'newPassword' in data:
                if 'currentPassword' not in data or not food_user.authenticate(data['currentPassword']):
                    return jsonify({'message': 'Current password is incorrect'}), 400
                food_user.password_hash = bcrypt.generate_password_hash(data['newPassword']).decode('utf-8')

            # Update other user attributes
            if 'username' in data:
                food_user.username = data['username']
            if 'email' in data:
                food_user.email = data['email']

            db.session.commit()
            return jsonify({'message': 'User updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 400
        
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
            data = request.get_json()
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
            data = request.get_json()
            user = FoodUser.query.filter(
                (FoodUser.username == data.get('username'))  
            ).first()

            if user and user.authenticate(data.get('password')):
                session['food_user_id'] = user.id
                return user.to_dict(), 200
            else:
                return {'message': 'Invalid Credentials'}, 403
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
        if "food_user_id" not in session:
            return {"message": "Not Authorized"}, 403
        if user := db.session.get(FoodUser, session["food_user_id"]):
            return user.to_dict(rules=("-email",)), 200
        return {"message": "Not Authorized"}, 403

api.add_resource(CheckSession, '/check_session') 

# Google OAuth routes
@app.route('/login/google', methods=["POST"])
def google_login():
    data = json.loads(request.data)
    req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={data['access_token']}",
        headers={"Content-Type": "text"})
    # redirect_uri = url_for('authorize', _external=True
    res=req.json()
    if res["verified_email"]:
        food_user = FoodUser.query.filter_by(email=res["email"]).first()
        if not food_user:
            food_user = FoodUser(username = res['name'], email = res['email'])
            food_user.password_hash = "password"
            db.session.add(food_user)
            db.session.commit()
        food_user=food_user.to_dict()
        session['food_user_id'] = food_user['id']
        return make_response(food_user, 200)
    return make_response({"message":"this doesnt work"}, 200)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('fooduserinfo')
    food_user_info = resp.json()
    food_user = FoodUser.query.filter_by(email=food_user_info['email']).first()

    if not food_user:
        food_user = FoodUser(email=food_user_info['email'], google_id=food_user_info['sub'])
        db.session.add(food_user)
        db.session.commit()

    access_token = create_access_token(identity=food_user.id)
    return jsonify(access_token=access_token), 200

@app.route('/current_user')
def current_user():
    food_user_id = session.get('food_user_id')
    if food_user_id:
        food_user = FoodUser.query.get(food_user_id)
        return jsonify(food_user.to_dict()), 200
    return jsonify(None), 401

# Error handler
@app.errorhandler(404)
def handle_404(error):
    return {'message': str(error)}, 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)