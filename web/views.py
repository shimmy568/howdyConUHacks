from models import db
from flask import Flask, render_template, make_response, redirect, Response, request, jsonify
from flask.views import MethodView
import time

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# my_file = os.path.join(BASE_DIR, 'myfile.txt')


class Index(MethodView):
    def get(self):
        # return Response(username+' user profile')
        # return make_response(render_template('html.html'), 200, {'Content-Type': 'text/html'})
        return render_template('index.html')
    
    def post(self):
        # print(request.form)
        # print(request.args)

        img = request.files.get('picture', '')

        if img:
            print('test')
        else:
            return make_response('error: no image uploaded', '500', {'Content-Type': 'text'})







        return make_response('success', '200', {'Content-Type': 'text'})