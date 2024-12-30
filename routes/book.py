from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import current_user, auth_token_required, roles_accepted

from models import db, section, Books, book_request,User, UserLibrary

#this is the api related to book section


#in book resource we can get the book and update the book and delete the book and create the book
class Book(Resource):
    @auth_token_required
    @roles_accepted("admin")
    def post(self):
        data = request.get_json()
        name = data["name"]
        author = data["author"]
        content = data["content"]
        section_id = data["section_id"]
        quantity = data["quantity"]
        
        check = Books.query.filter_by(name=name).first()
        if not check:
            new_book = Books(name=name, author=author,
                             content=content, section_id=section_id, quantity=quantity)
            db.session.add(new_book)
            if current_user.has_role("admin"):
                new_book.status = True
            db.session.commit()
            return make_response(jsonify({"message": "Book is created successfully", "book_id": new_book.id}), 201)
        return make_response(jsonify({"message": "Book is already present"}), 409)
    def get(self):
        data = Books.get_all_books()
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Book found"}), 404)

    
    def put(self, book_id):
        data = request.get_json()
        Nname = data["Nname"]
        description = data["description"]
        author = data["author"]
        section_id = data["section_id"]
        quantity = data["quantity"]
        
        book = Books.query.filter_by(id=book_id).first()
        if book:
            book.name = Nname
            book.description = description
            book.author = author
            book.section_id = section_id
            book.quantity = quantity
            if current_user.has_role("admin"):
                book.status = True
            db.session.commit()
            return make_response(jsonify({"message": "Book is updated successfully", "book_id": book.id}), 201)
        return make_response(jsonify({"message": "Book is not present"}), 404)




    def delete(self):
        data = request.get_json()
        id = data["id"]
        book = Books.query.filter_by(id=id).first()
        if book:
            db.session.delete(book)
            db.session.commit()    
            return make_response(jsonify({"message": "Book is uodated successfully", "book_id": book.id}), 201)
        return make_response(jsonify({"message": "Book is not present"}), 404)
    



#in this section we are dealing with book request from user

class BookRequest(Resource):
    #this will make sure that a user have max of 5 books
    MAX_BOOKS_PER_USER = 5

    #this is for the user to make a book request
    @auth_token_required
    def post(self):
        data = request.get_json()
        book_id = data.get("book_id")
        user_id = current_user.id

        user_library_count = UserLibrary.query.filter_by(user_id=user_id).count()
        if user_library_count >= self.MAX_BOOKS_PER_USER:
            return make_response(jsonify({"message": "You cannot have more than 5 books in your library"}), 403)

        existing_request = book_request.query.filter_by(book_id=book_id, user_id=user_id, status=False ).first()
        if existing_request:
            return make_response(jsonify({"message": "You have already requested this book"}), 409)

        new_request = book_request(book_id=book_id, user_id=user_id)
        db.session.add(new_request)
        db.session.commit()
        return make_response(jsonify({"message": "Book request sent successfully"}), 201)

    #this is for the admin to approve the book request
    @auth_token_required
    def put(self, request_id):
        book_request_instance = book_request.query.filter_by(id=request_id).first()
        if book_request_instance:
            book_request_instance.status = True

            # Add book to user's library
            user_library = UserLibrary(user_id=book_request_instance.user_id, book_id=book_request_instance.book_id)
            db.session.add(user_library)

            # Reduce the book quantity by 1
            book = Books.query.get(book_request_instance.book_id)
            if book.quantity > 0:
                book.quantity -= 1
                db.session.commit()
            else:
                return make_response(jsonify({"message": "Book out of stock"}), 409)

            db.session.commit()
            return make_response(jsonify({"message": "Book request approved and added to library"}), 200)
        return make_response(jsonify({"message": "Book request not found"}), 404)

    #this is for the admin to deny the book request
    @auth_token_required
    def delete(self, request_id):
        book_request_instance = book_request.query.filter_by(id=request_id).first()
        if book_request_instance:
            db.session.delete(book_request_instance)
            db.session.commit()
            return make_response(jsonify({"message": "Book request denied"}), 200)
        return make_response(jsonify({"message": "Book request not found"}), 404)

    #this is for the admin to get all the book request
    @auth_token_required
    def get(self):
        requests = book_request.query.filter_by(status=False).all()
        requests_data = []
        for req in requests:
            user = User.query.get(req.user_id)
            book = Books.query.get(req.book_id)
            requests_data.append({
                'id': req.id,
                'book': book.serialize(),
                'user': user.serialize(),
                'request_date': req.request_date,
                'status': req.status
            })
        return jsonify({'data': requests_data})


#this is the api for the user library
class UserLibraryAPI(Resource):
    @auth_token_required
    def get(self):
        user_id = current_user.id
        user_library_entries = UserLibrary.get_books_by_user_id(user_id)
        books = []
        for entry in user_library_entries:
            book = Books.query.filter_by(id=entry.book_id).first()
            if book:
                books.append(book.serialize())
        return jsonify({'data': books})

#this is the api for the user to return the book
class ReturnBook(Resource):
    @auth_token_required
    def delete(self, book_id):
        user_id = current_user.id
        user_library_entry = UserLibrary.query.filter_by(user_id=user_id, book_id=book_id).first()

        if user_library_entry:
            db.session.delete(user_library_entry)
            book = Books.query.filter_by(id=book_id).first()
            if book:
                book.quantity += 1
                db.session.commit()
            return jsonify({"message": "Book returned successfully"})  # Return a dictionary, not a Response

        return jsonify({"message": "Book not found in user's library"}), 404  # Return a dictionary, not a Response


