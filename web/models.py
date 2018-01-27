from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# secret_key =     
    

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
