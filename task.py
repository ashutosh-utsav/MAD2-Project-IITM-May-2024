from celery import shared_task
from celery import current_task
from models import User, Books, section, book_request, Role, UserLibrary
import flask_excel as excel
from send_mail import send_email
from jinja2 import Template
from datetime import datetime, timedelta


#this is for monthly reminder
@shared_task(ignore_result=False)
def monthly_reminder():
    admin_role = Role.query.filter_by(name='admin').first()

   
    admin = User.query.filter(User.roles.contains(admin_role)).first()

    if not admin:
        print("No admin user found.")
        return "No admin user found."

    
    with open('report.html', 'r') as file:
        template = Template(file.read())
        

    total_books = Books.query.count()
    total_users = User.query.count()
    total_sections = section.query.count()
    total_requests = book_request.query.count()

   
    send_email(
        admin.email,
        "Monthly Report",
        template.render(
            total_books=total_books,
            total_users=total_users,
            total_sections=total_sections,
            total_requests=total_requests
        )
    )
    return "Monthly report sent to admin."


from json import dumps
from httplib2 import Http

#this is for daily reminder

@shared_task(ignore_result=False)
def daily_reminder():
    try:
  
        timestamp = datetime.utcnow() - timedelta(hours=24)

        #this is for if user have not visited the app in last 24 hours
        # not_visited_users = User.query.filter(User.last_login_at < timestamp).all()

        #this is for checking
        not_visited_users = User.query.filter(User.last_login_at < datetime.utcnow()).all()
        if not not_visited_users:
            return "no inactive users today"

        for user in not_visited_users:
            username = user.username
            if username != 'admin':
                send_notification(username)

        return "Notifications sent to google chat space"
    except Exception as e:
        print(f"Error in daily_reminder task: {e}")
        return f"Error in daily_reminder task: {e}"

def send_notification(username):
    try:
        #this is the google chat webhook url
        url = "https://chat.googleapis.com/v1/spaces/AAAAdkYwjc0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=DWjOxYW_rnMiY_AkdtiFR-zhlOBHlTkFT8XDPdWINm4"
        app_message = {"text": f"Hello {username}! You haven't visited web library today. Please visit the app and read some Book."}
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )
        return f"Notification sent to {username}"
    except Exception as e:
        print(f"Error in send_notification task: {e}")
        return f"Error in send_notification task: {e}"
    



