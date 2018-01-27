from flask import Flask, g, render_template, make_response, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask.views import View
from flask_login import LoginManager
from models import db, User

import random, string, time


#CONFIG AND INIT
app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #This adds signifcant overhead
app.secret_key = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in range(32))
app.config['SESSION_TYPE'] = 'filesystem'
with app.app_context():
    db.init_app(app)



def init_db():
    print("init db")
    with app.app_context():
        db.create_all()
        new_user = User(username='loc', password=generate_password_hash('1'), email='email')#gcacadmin, gcacadminpassword123
        db.session.add(new_user)
        db.session.commit()

from views import Index, Login, Logout, Register, Admin, UserPage, SaveProfile

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))

app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
# app.add_url_rule('/register', view_func=Register.as_view('register'))
app.add_url_rule('/', view_func=Index.as_view('index'))
app.add_url_rule('/admin', view_func=Admin.as_view('admin'))

app.add_url_rule('/save', view_func=SaveProfile.as_view('Save Profile'))
app.add_url_rule('/<username>', view_func=UserPage.as_view('User Page'))

#API

if __name__ == '__main__':
    app.run(debug=True)

