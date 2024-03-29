# coding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

from app import views, models
from app.admin_views import admin
app.register_blueprint(admin)
