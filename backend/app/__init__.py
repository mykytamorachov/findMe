# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

app = Flask(__name__)
UPLOAD_FOLDER = '/Users/air13/Desktop/findMe/app/static/img'
#UPLOAD_FOLDER = '/var/lib/thatriff/backend/that_riff/app/static/img'
EXPORTS_URL = '/static/exports'
EXPORTS_FOLDER = '/Users/air13/Desktop/findMe/app/static/exports'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'gif', 'jpeg'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/findme'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Vakoms4ever!@localhost/thatriff'
app.secret_key = "\xa7\xab\x87\xd7\xff\xdc\xae \x0cY\x87\xf9t\xea\x19\t\x0eN\xe9\xea\xe8\xb6\xd6>"
db = SQLAlchemy(app)

FACEBOOK_APP_ID = '186009311594204'
FACEBOOK_APP_SECRET = '1f70984f264c77327c5df14f54a54a88'

app.config.update(
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'lavriv92@gmail.com',
	MAIL_PASSWORD = 'nightwish1992',
	STATIC_URL = "http:/127.0.0.1:5000/static/"
	)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mail = Mail(app)
from app import views