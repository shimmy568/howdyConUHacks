from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_login import UserMixin
import time
db = SQLAlchemy()

# secret_key =     
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    time = db.Column(db.Integer, nullable=False, default=time.time())
    facebook = db.Column(db.String(100), default="")
    twitter = db.Column(db.String(100), default="")
    instagram = db.Column(db.String(100), default="")

    def __repr__(self):
        return str(self.username)
        
    @classmethod
    def verify_password(self, password, password_hash):
        return check_password_hash(password_hash, password)

    @classmethod
    def username_taken(self, username):
        return db.session.query(db.exists().where(User.username==username)).scalar()
    

    # @classmethod
    # def email_taken(self, email):
    #     return db.session.query(db.exists().where(User.email==email)).scalar()

# class PDF(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=False, nullable=False)
#     data = db.Column(db.LargeBinary)
#     def __repr__(self):
#         # print(self.data)
#         return str(self.name)
