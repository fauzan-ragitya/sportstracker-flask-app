#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from camera import VideoCamera
from flask_socketio import SocketIO
from flask_socketio import emit
import json

app = Flask(__name__)
camera = VideoCamera()
socketio = SocketIO(app)


def gen(type):
    camera.select_type(type)
    while True:
        #timer
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

'''Main Page, Mode=None'''
@app.route('/')
def index():
    return render_template('index.html', count=0, conf_level=0)

@app.route('/video_feed')
def video_feed():
    return Response(gen(None),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

'''Pushup page, Mode=pushup'''
@app.route('/pushup', methods = ['GET', 'POST'])
def pushup_index():
    return render_template('index_pushup.html')

@app.route('/video_feed_pushup')
def video_feed_pushup():
    camera.reset()
    return Response(gen(type='pushup'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

'''Situp page, Mode=situp'''
@app.route('/situp')
def situp_index():
    
    return render_template('index_situp.html')

@app.route('/video_feed_situp')
def video_feed_situp():
    camera.reset()
    return Response(gen(type='situp'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

'''Pullup page, Mode=pullup'''
@app.route('/pullup')
def pullup_index():
    return render_template('index_pullup.html')

@app.route('/video_feed_pullup')
def video_feed_pullup():
    camera.reset()
    return Response(gen(type='pullup'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # socketio.run(app)