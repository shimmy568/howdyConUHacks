from flask import Flask, g, render_template, make_response, redirect
from flask.views import View

import random, string, time


#CONFIG AND INIT
app = Flask(__name__)
app.config['DEBUG'] = False

#SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #This adds signifcant overhead
# with app.app_context():
#     db.init_app(app)



app.secret_key = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in range(32))
app.config['SESSION_TYPE'] = 'filesystem'



# def init_db():
#     print("init db")
#     with app.app_context():
#         db.create_all()
#         db.session.commit()

from views import Index 

# app.add_url_rule('/register', view_func=Register.as_view('register'))

app.add_url_rule('/', view_func=Index.as_view('Index'))

#API

if __name__ == '__main__':
    app.run(debug=True)

