from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, auth_token_required, roles_accepted

from models import db, section, Books

#this is the api related to book section admin can create, edit, delete and get the section

class Section(Resource):
    @auth_token_required
    @roles_accepted("admin")
    def post(self):
        data = request.get_json()
        name = data["name"]
        description = data["description"]
        userid = current_user.id
        print(userid)
        check = section.query.filter_by(name=name).first()
        if not check:
            new_cat = section(name=name, description=description)
            db.session.add(new_cat)
            if current_user.has_role("admin"):
                new_cat.status = True
            db.session.commit()
            return make_response(jsonify({"message": "section is created successfully", "section_id": new_cat.id}), 201)
        return make_response(jsonify({"message": "section is already present"}), 409)
    
    
    def get(self, section_id=None):
        if section_id:
            sec = section.get_section_by_id(section_id)
            if sec:
                books = Books.get_books_by_section_id(section_id)
                books_data = [book.serialize() for book in books]
                
                return make_response(jsonify({"section": sec.serialize(), "books": books_data}), 200)
            return make_response(jsonify({"message": "Section not found"}), 404)
        else:
            data = section.get_all_section()
            if data:
                final_data = [sec.serialize() for sec in data]
                return make_response(jsonify({"data": final_data}), 200)
            return make_response(jsonify({"message": "No sections found"}), 404)



    def put(self):
        data = request.get_json()
        id = data["id"]
        name = data["name"]
        description = data["description"]
        cate = section.query.filter_by(id=id).first()
        if cate:
            cate.name = name
            cate.description = description
            if current_user.has_role("admin"):
                cate.status = True
            db.session.commit()
            return make_response(jsonify({"message": "section is updated successfully", "section_id": cate.id}), 200)
        return make_response(jsonify({"message": "section is not present"}), 404)
    
    def delete(self, section_id):
        cate = section.query.filter_by(id=section_id).first()
        if cate:
            db.session.delete(cate)
            db.session.commit()    
            return make_response(jsonify({"message": "Section deleted successfully", "section_id": cate.id}), 201)
        return make_response(jsonify({"message": "Section not present"}), 404)

    
    def patch(self, id):
        print("test")
        section = section.query.filter_by(id=id).first()
        return make_response(jsonify({"message": "section found", "id": section.id}), 200)
