from models import db, User
from flask import Flask, render_template, make_response, redirect, Response, request, jsonify
from flask.views import MethodView
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug import secure_filename
import time

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# my_file = os.path.join(BASE_DIR, 'myfile.txt')

class SaveProfile(MethodView):
    @login_required
    def get(self):
        return make_response(render_template('edit.html'), 200, {'Content-Type': 'text/html'})
    @login_required
    def post(self):
        # print(request.form)
        # user = db.session.query(User).filter_by(username=current_user).first()
        user = current_user

        if request.form['facebook'] != "":
            user.facebook = request.form['facebook']
        if request.form['twitter'] != "":
            user.twitter = request.form['twitter']
        if request.form['instagram'] != "":
            user.instagram = request.form['instagram']

        db.session.commit()

        return Response('success')
        # return Response(request.args)

class UserPage(MethodView):
    def get(self, username):
        user = db.session.query(User).filter_by(username=username).first()

        # return Response(username+' user profile')
        return make_response(render_template('userpage.html', facebook=user.facebook, twitter=user.twitter, instagram=user.instagram), 200, {'Content-Type': 'text/html'})

class Index(MethodView):
    def get(self, username):
        # return Response(username+' user profile')
        return make_response(render_template('index.html'), 200, {'Content-Type': 'text/html'})

class Register(MethodView):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html', errors=[]), 200, headers)

    def post(self):
        print('register post')
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
        except Exception as e:
            print(e)
            pass

        print("register", username, password, email)

        headers = {'Content-Type': 'text/html'}
        errors = []
        success = True
        if len(password) < 8:
            # return ('password is too short (8 or more characters)', 412)
            errors.append('password is too short (8 or more characters)')
            success = False

        if not username:
            errors.append('no username provided')
            success = False

        if not password:
            errors.append('no password provided')
            success = False

        if not email:
            errors.append('no email provided')
            success = False

        if User.username_taken(username):
            return ('username is not unique', 412)
            errors.append('username is not unique')
            success = False

        try:
            new_user = User(username=username, password=generate_password_hash(password), email=email)
        except Exception as e:
            # print(e)
            # print('couldnt create new user')
            errors.append('server error')
            success = False

        if success:
            try:
                db.session.add(new_user)
            except:
                print('couldnt session cant add')
                return make_response(render_template('error.html', e=500), 200, headers)
            try:
                db.session.commit()
                return ('successfully registered', 200)
            except:
                print('couldnt commit')
                return make_response(render_template('error.html', e=500), 200, headers)
        else:
            return make_response(render_template('register.html', errors=errors), 200, headers)


class Login(MethodView):

    def get_template_name(self):
        raise NotImplementedError()

    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = None

        headers = {'Content-Type': 'text/html'}
        errors = []

        # print(username, password)
        try:
            user = db.session.query(User).filter_by(username=username).first()
            print(user)
        except:
            # return Response("user name not recognized")
            errors.append('no user named %s' %username)

        if not username or not password:
            errors.append('insure that username and password are not blank')

        # if notL user:
            # return Response('no user named %s'%username)
            # errors.append('no user named %s'%username)
        try:
            if  user.verify_password(password, user.password) and username and password:
                login_user(user)
                return redirect(request.args.get("next"))
                # return Response('logged in')
            else:
                errors.append('password or username is incorrect')
        except:
            errors.append('password or username is incorrect')

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html', errors=errors), 200, headers)

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html', errors=[]), 200, headers)


class Logout(MethodView):
    @login_required
    def get(self):
        logout_user()
        return Response('<p>Logged out</p>')

class Admin(MethodView):
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('admin.html'), 200, headers)