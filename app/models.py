# coding: utf-8
from app import db

class User(db.Model):

    CONFIRMATION_FALSE = 0
    CONFIRMATION_TRUE = 1

    ROLE_USER = 0
    ROLE_ADMIN = 1

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(200))
    instalink = db.Column(db.String(250))
    skype = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    user_role = db.Column(db.SmallInteger(2), default=ROLE_USER)
    password = db.Column(db.String(20))
    confirmation = db.Column(db.SmallInteger(2), default=CONFIRMATION_FALSE)
    EmailConfirmation = db.relationship('EmailConfirmation', backref= db.backref('conf', cascade='all'), lazy = 'dynamic')


class EmailConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    hash_confirm = db.Column(db.String(100))



