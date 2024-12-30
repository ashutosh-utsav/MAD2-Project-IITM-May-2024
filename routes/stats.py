from flask import jsonify
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from models import db, User, Books, section, book_request


#this is the api for the admin to get all the stats of the web app
class AppStats(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        total_users = User.query.count()
        total_books = Books.query.count()
        total_sections = section.query.count()
        total_requests = book_request.query.count()
        approved_requests = book_request.query.filter_by(status=True).count()
        denied_requests = total_requests - approved_requests
        pending_requests = book_request.query.filter_by(status=False).count()

        stats = {
            'totalUsers': total_users,
            'totalBooks': total_books,
            'totalSections': total_sections,
            'totalRequests': total_requests,
            'approvedRequests': approved_requests,
            'deniedRequests': denied_requests,
            'pendingRequests': pending_requests
        }

        return jsonify(stats)


