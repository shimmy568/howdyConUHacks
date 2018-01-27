from models import db
from flask import Flask, render_template, make_response, redirect, Response, request, jsonify
from flask.views import MethodView
import time

from utils import translate, detect_text

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

        img = request.files.get('img')
        y1 = request.files.get('y1')
        y2 = request.files.get('y2')
        x1 = request.files.get('x1')
        x2 = request.files.get('x2')

        if img:
            #crop image
            
            #text from OCR
            aws_return = detect_text(img)
            # text = "a fine Abbacchio with a side of Amaretti topped with fresh shavings of Noce Moscata Bao bun"

            translate(aws_return['DetectedText'])


        else:
            return make_response('error: no image uploaded', '500', {'Content-Type': 'text'})







        return make_response('success', '200', {'Content-Type': 'text'})