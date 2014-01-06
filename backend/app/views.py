# -*- coding: utf-8 -*-

from flask import request, Response, abort, \
    render_template, redirect, url_for, session
from flask.ext.mail import Message
from geopy import point, distance
from sqlalchemy import and_, or_
from json import dumps, loads
from app import *
import math
from models import *
import hashlib
import string
from urllib import urlopen
from random import choice
import os
import re
import urllib
from datetime import datetime

def to_md5(string):
    h = hashlib.new('md5')
    h.update(string)
    return h.hexdigest()

def generate_passwd():
    chars = string.letters + string.digits
    newpasswd = ''
    for i in range(8):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register_with_facebook', methods=['POST', 'GET'])
def register_with_facebook():
    if request.method == 'POST':
        try:
            request_data = loads(request.data)
            url_string = 'https://graph.facebook.com/me?access_token=%s' % request_data['access_token']
            fb_data = urlopen(url_string).read()
            fb_data = loads(fb_data)

            duser = User.query.filter_by(username=fb_data["username"]).first()

            if duser is None:
                password = generate_passwd()

                user = User(
                    fb_data["name"],
                    fb_data["username"],
                    fb_data["email"],
                    request_data['latitude'],
                    request_data['longitude'],
                    fb_data['id'],
                    'Facebook'
                    )
                db.session.add(user)
                db.session.commit()
                response = {
                    'ansCode':1,
                    'UID': user.id
                }
            else:
                response = {
                    'ansCode':1,
                    'UID': duser.id
                }
        except:
            response = {
                'ansCode':99,
                'Error':'Wrong params'
            }
        return Response(
            response=dumps(response),
            status=200,
            headers={
                'Content-Type':'application/json'
            })
    else:
        abort(404)

@app.route('/update_coordinates', methods=['POST', 'GET'])
def update_coordinates():
    if request.method == 'POST':
        try:
            request_data = loads(request.data)
            id = request_data['user_id']
            lat = request_data['latitude']
            long = request_data['longitude']
            user = User.query.filter_by(social_id=id)
            user.latitude = lat
            user.longitude = long
            db.session.commit()
            response = {
                'status': 1
            }
        except:
            response = {
                'ansCode': 99,
                'Error': 'Wrong params'
            }
        return Response(
            response=dumps(response),
            status=200,
            headers={
                'Content-Type': 'application/json'
            })
    else:
        abort(404)

def findPeopleinKm():
    if request.method == 'POST':
        try:
            request_data = loads(request.data)
            dist = 20 #дистанция 20 км
            mylon = request_data['longitude'] # долгота центра
            mylat = request_data['latitude'] # широта
            lon1 = mylon-dist/abs(math.cos(math.radians(mylat))*111.0) # 1 градус широты = 111 км
            lon2 = mylon+dist/abs(math.cos(math.radians(mylat))*111.0) # 1 градус долготы тоже :)
            lat1 = mylat-(dist/111.0)
            lat2 = mylat+(dist/111.0)
            users = User.query.filter(and_(User.latitude.between(lat1, lat2), (User.longitude.between(lon1, lon2))))
            response = {
                'status': 1,
                'users': users
            }
        except:
            response = {
                'ansCode': 99,
                'Error': 'Wrong params'
            }
        return Response(
            response=dumps(response),
            status=200,
            headers={
                'Content-Type': 'application/json'
            })
    else:
        abort(404)
    return True