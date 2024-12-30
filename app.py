from flask import request
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_security import Security
from models import db, user_datastore
from cacher import cache
from worker import celery_init_app
from celery.schedules import crontab
from mailconfig import Config
from task import monthly_reminder, daily_reminder

from extensions import mail

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.localDev")
    app.config.from_object(Config)

    db.init_app(app)
    
    security = Security(app, user_datastore)

    CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    cache.init_app(app)

    api = Api(app)

    mail.init_app(app)

    return app, api

app, api_handler = create_app()
celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def celery_job(sender, **kwargs):
    # sender.add_periodic_task(crontab(hour=8, minute=0, day_of_month=1), monthly_reminder.s())
    # sender.add_periodic_task(crontab(hour=18, minute=0), daily_reminder.s())

    # for testing
    sender.add_periodic_task(60, monthly_reminder.s())
    sender.add_periodic_task(10, daily_reminder.s())


@app.route("/hello_world")
def hello_world():
    return "Hello World!"

# Import routes
from routes.auth import Signin, Signup
api_handler.add_resource(Signin, "/signin")
api_handler.add_resource(Signup, "/signup")

from routes.section import Section 
api_handler.add_resource(Section, "/book_section", "/book_section/<int:section_id>")

from routes.book import Book, BookRequest, UserLibraryAPI, ReturnBook
api_handler.add_resource(Book, "/book", "/book/<int:book_id>")
api_handler.add_resource(BookRequest, '/request_book', '/request_book/<int:request_id>')
api_handler.add_resource(ReturnBook, '/return_book/<int:book_id>')


from routes.user_library import UserLibraryEndpoint, AdminUserLibrary
api_handler.add_resource(UserLibraryEndpoint, '/user_library')
api_handler.add_resource(AdminUserLibrary, '/admin_user_library/<int:user_id>', '/admin_user_library/<int:book_id>/<int:user_id>')

from routes.stats import AppStats
api_handler.add_resource(AppStats, '/app-stats')

from routes.user_management import UserManagement
api_handler.add_resource(UserManagement, '/users', '/users/<int:user_id>')

from routes.search import Search
api_handler.add_resource(Search, '/search')




from routes.export import export_bp
app.register_blueprint(export_bp)





if __name__ == "__main__":
    app.run(debug=True, port=3000)
