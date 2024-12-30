from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import login_user, verify_password

from models import db, user_datastore


#here is the api for login and signup

class Signin(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        
        user = user_datastore.find_user(email=email)
        if user:
            if verify_password(password, user.password):
                token = user.get_auth_token()
                if token:
                    login_user(user)
                    db.session.commit()
                return make_response(jsonify({"message": "login successful", "authToken": token, "email": user.email, "role": user.roles[0].name, "id": user.id}), 200)
            else:
                return make_response(jsonify({"message": "invalid password"}), 401)        
        return make_response(jsonify({"message": "user not found", "email": user.email}), 404)
    
class Signup(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        username = data['username']
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        if not username:
            return make_response(jsonify({"message": "username is required"}), 400)
        
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "user already exists", "email": email}), 409)
        
        user = user_datastore.create_user(email=email, password=password, username=username)
        
        user_datastore.add_role_to_user(user, "user")
        db.session.commit()
        return make_response(jsonify({"message": "user created", "id": user.id, "email": user.email}), 201)