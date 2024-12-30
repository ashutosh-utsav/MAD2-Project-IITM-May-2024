from flask import jsonify, make_response
from flask_restful import Resource
from flask_security import auth_token_required, current_user
from models import db, UserLibrary, Books, User


class UserLibraryEndpoint(Resource):
    @auth_token_required
    def get(self):
        user_id = current_user.id
        user_library = UserLibrary.get_books_by_user_id(user_id)
        books = [Books.query.filter_by(id=item.book_id).first().serialize() for item in user_library]
        return make_response(jsonify({"data": books}), 200)
    

#this api is for admin to see and delete a book from user library
class AdminUserLibrary(Resource):
    @auth_token_required
    def get(self, user_id):
        user_library = UserLibrary.get_books_by_user_id(user_id)
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        books = [Books.query.filter_by(id=item.book_id).first().serialize() for item in user_library]
        return make_response(jsonify({"username": user.username, "books": books}), 200)
    
    @auth_token_required
    def delete(self, book_id, user_id):
        user_library_entry = UserLibrary.query.filter_by(user_id=user_id, book_id=book_id).first()
        if user_library_entry:
            db.session.delete(user_library_entry)
            book = Books.query.filter_by(id=book_id).first()
            if book:
                book.quantity += 1
                db.session.commit()
            return jsonify({"message": "Book revoked successfully"}), 200

        return jsonify({"message": "Book not found in user's library"}), 404