# coding: utf-8
from app import db

class User(db.Model):

    CONFIRMATION_FALSE = 0
    CONFIRMATION_TRUE = 1

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(200))
    instalink = db.Column(db.String(250))
    skype = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    confirmation = db.Column(db.SmallInteger(2), default=CONFIRMATION_FALSE)
    EmailConfirmation = db.relationship('EmailConfirmation', backref= db.backref('conf', cascade='all'), lazy = 'dynamic')

    #def __init__(self, name, phone, whatsapp, email, instalink, skype, comment, confirmation):
     #   pass


class EmailConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    hash_confirm = db.Column(db.String(100))



