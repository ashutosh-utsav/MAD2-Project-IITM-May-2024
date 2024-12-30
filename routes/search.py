from flask import request, jsonify
from flask_restful import Resource
from models import Books, section

class Search(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        books = Books.query.filter(Books.name.ilike(f"%{query}%")).all()
        sections = section.query.filter(section.name.ilike(f"%{query}%")).all()
        
        books_data = [book.serialize() for book in books]
        sections_data = [sec.serialize() for sec in sections]

        return jsonify({
            "books": books_data,
            "sections": sections_data
        })
