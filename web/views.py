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
        y1 = int(request.form.get('y1', '0'))
        y2 = int(request.form.get('y2', '500'))
        x1 = int(request.form.get('x1', '0'))
        x2 = int(request.form.get('x2', '500'))

        # print(img)
        # im = b64decode(img)
        # im = Image(img)


        # im = Image.open(BytesIO(base64.b64decode(img+ "========")))
        # print(im)


        if img:
        #     #crop image
                    # print(img[0:100], img[-100:])
            im = Image.open(BytesIO(base64.b64decode(img)))
            # print(im)
            # print(type(im))
            # im.save("img4.png")

            im = im.crop((x1, y1, x2, y2))
            # im.save("img.png")

            # with BytesIO() as output:
                # im.save(output, 'BMP')
                # b_img = output.getvalue()

            aws_return = detect_text(b_img)
            # aws_return = detect_text('test_ocr.png')
            # print(aws_return)

        #     #text from OCR
        #     aws_return = detect_text(img)
        #     # text = "a fine Abbacchio with a side of Amaretti topped with fresh shavings of Noce Moscata Bao bun"

        #     translate(aws_return['DetectedText'])


        else:
            return make_response('error: no image uploaded', '500', {'Content-Type': 'text'})







        return make_response('success', '200', {'Content-Type': 'text'})