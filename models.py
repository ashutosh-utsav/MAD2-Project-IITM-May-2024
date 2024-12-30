from flask_security import UserMixin, RoleMixin, AsaList, SQLAlchemyUserDatastore
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'last_login_ip': self.last_login_ip,
            'current_login_ip': self.current_login_ip,
            'login_count': self.login_count,
            'active': self.active,
            'fs_uniquifier': self.fs_uniquifier,
            'confirmed_at': self.confirmed_at
        }
    def get_all_users():
        return User.query.all()
    
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class section(db.Model):
    __tablename__ = 'section'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now())


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at
            
        }
    
    def get_all_section():
        data = section.query.all()
        if data:
            return data
        return False
    
    def get_section_by_id(id):
        return section.query.filter_by(id=id).first()
    
    def admin_delete(id):
        section = section.query.filter_by(id=id).first()
        db.session.delete(section)
        db.session.commit()
        if section.query.filter_by(id=id).first() == None:
            return True
        return False
    
    def manager_delete(id):
        section = section.query.filter_by(id=id).first()
        section.delete = True
        db.session.commit()
        if section.query.filter_by(id=id).first().delete == True:
            return True
        return False
    

class Books(db.Model):
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    author = Column(String(255), nullable=False)
    date_added = Column(DateTime(), default=datetime.now())
    section_id = Column(Integer(), ForeignKey('section.id'))
    content = Column(String(512))
    quantity = Column(Integer(), default=5)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'date_added': self.date_added,
            'section_id': self.section_id,
            'content': self.content,
            'quantity': self.quantity 
        }
    def get_all_books():
        return Books.query.all()
    def get_book_by_id(id):
        return Books.query.filter_by(id=id).first()
    def get_books_by_section_id(section_id):
        return Books.query.filter_by(section_id=section_id).all()
    def admin_delete(id):
        book = Books.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
        if Books.query.filter_by(id=id).first() == None:
            return True
        return False

class book_request(db.Model):
    id = Column(Integer(), primary_key=True)
    book_id = Column(Integer(), ForeignKey('books.id'))
    user_id = Column(Integer(), ForeignKey('user.id'))
    request_date = Column(DateTime(), default=datetime.now())
    status = Column(Boolean(), default=False)
    def serialize(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'request_date': self.request_date,
            'status': self.status
        }
    def get_all_requests():
        return book_request.query.all()
    def get_request_by_id(id):
        return book_request.query.filter_by(id=id).first()
    def get_request_by_user_id(user_id):
        return book_request.query.filter_by(user_id=user_id).all()
    def get_request_by_book_id(book_id):
        return book_request.query.filter_by(book_id=book_id).all()
    def admin_delete(id):
        book = book_request.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
        if book_request.query.filter_by(id=id).first() == None:
            return True
        return False
    def admin_approve(id):
            book = book_request.query.filter_by(id=id).first()
            book.status = True
            db.session.commit()
            if book_request.query.filter_by(id=id).first().status == True:
                # Add the book to the user's library
                user_library = UserLibrary(user_id=book.user_id, book_id=book.book_id)
                db.session.add(user_library)
                db.session.commit()
                return True
            return False
    def admin_reject(id):
        book = book_request.query.filter_by(id=id).first()
        book.status = False
        db.session.commit()
        if book_request.query.filter_by(id=id).first().status == False:
            return True
        return False
    def user_request_book(book_id, user_id):
        book = book_request(book_id=book_id, user_id=user_id)
        db.session.add(book)
        db.session.commit()
        if book_request.query.filter_by(book_id=book_id, user_id=user_id).first() == book:
            return True
        return False
    def user_delete_request(id):
        book = book_request.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
        if book_request.query.filter_by(id=id).first() == None:
            return True
        return False
    def user_get_request_by_id(id):
        return book_request.query.filter_by(id=id).first()
    
class UserLibrary(db.Model):
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id'))
    book_id = Column(Integer(), ForeignKey('books.id'))
    added_date = Column(DateTime(), default=datetime.now())

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'added_date': self.added_date
        }

    @staticmethod
    def get_books_by_user_id(user_id):
        return UserLibrary.query.filter_by(user_id=user_id).all()
