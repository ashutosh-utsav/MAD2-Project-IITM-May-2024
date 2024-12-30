from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from models import db, User, UserLibrary

#this is the api for admin to manage the users
class UserManagement(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        users = User.query.all()
        users_data = [user.serialize() for user in users]
        return jsonify({'data': users_data})

    @auth_token_required
    @roles_accepted('admin')
    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            UserLibrary.query.filter_by(user_id=user_id).delete()  # Delete user's library entries first
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "User deleted successfully"}), 200)
        return make_response(jsonify({"message": "User not found"}), 404)
