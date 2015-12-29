# coding: utf-8

from flask import Flask
from app.admin_views import admin
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')
app.register_blueprint(admin)
db = SQLAlchemy(app)


from app import views, models
