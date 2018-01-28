from models import db
from flask import Flask, render_template, make_response, redirect, Response, request, jsonify
from flask.views import MethodView
import time

from utils import translate, detect_text

import os


#images
from PIL import Image
import base64
from io import BytesIO


import json

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

        img = request.form.get('img')
        y = int(request.form.get('y', '0'))
        h = int(request.form.get('height', '500'))
        x = int(request.form.get('x', '0'))
        w = int(request.form.get('width', '500'))


        print(y,h,x,w)
        # print(img)
        # im = b64decode(img)
        # im = Image(img)


        # im = Image.open(BytesIO(base64.b64decode(img+ "========")))
        # print(im)


        if img:
        #     #crop image
            im = Image.open(BytesIO(base64.b64decode(img)))


            im = im.crop((x, y, x+w, y+h))
            im.save("out.png")

            with open('out.png', "rb") as imageFile:
                
                f = imageFile.read()
                b_img = bytearray(f)


            aws_return = detect_text(b_img)

            words = ""
            for line in (aws_return['TextDetections']):
                words = words + ' ' + line.get('DetectedText', '')
            
            # print(translate(words))
            return jsonify(translate(words))
            # print(words)

        else:
            return make_response('error: no image uploaded', '500', {'Content-Type': 'text'})







        # return make_response('success', '200', {'Content-Type': 'text'})