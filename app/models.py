# coding: utf-8
from app import db

WORKING_FALSE = 0
WORKING_TRUE = 1

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
    EmailConfirmation = db.relationship('EmailConfirmation', backref=db.backref('conf'), lazy='dynamic')



class EmailConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), ondelete="CASCADE", onupdate='CASCADE')
    hash_confirm = db.Column(db.String(100))


class InstaUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    insta_id = db.Column(db.BigInteger, unique=True)


class LikingTagJob(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    insta_user_id = db.Column(db.Integer, db.ForeignKey('instauser.id'), ondelete="CASCADE", onupdate='CASCADE')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sleep_param = db.Column(db.SmallInteger(3))
    num_likes = db.Column(db.Integer)
    working = db.Column(db.SmallInteger(2), default=WORKING_FALSE)

  #TODO: NEED TABLE OF COMPETITOR
class LikingCompetitorJob(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    insta_user_id = db.Column(db.Integer, db.ForeignKey('instauser.id'), ondelete="CASCADE", onupdate='CASCADE')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sleep_param = db.Column(db.SmallInteger(3))
    num_likes = db.Column(db.SmallInteger)
    num_users = db.Column(db.Integer)
    competitor_name = db.Column(db.String(50))
    competitor_id = db.Column(db.BigInteger, index=True)
    working = db.Column(db.SmallInteger(2), default=WORKING_FALSE)


class SubscriptTagJob(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    insta_user_id = db.Column(db.Integer, db.ForeignKey('instauser.id'), ondelete="CASCADE", onupdate='CASCADE')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sleep_param = db.Column(db.SmallInteger(3))
    num_likes = db.Column(db.SmallInteger)
    num_users = db.Column(db.Integer)
    working = db.Column(db.SmallInteger(2), default=WORKING_FALSE)


#TODO: NEED TABLE OF COMPETITOR
class SubscriptCompetitorJob(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    insta_user_id = db.Column(db.Integer, db.ForeignKey('instauser.id'), ondelete="CASCADE", onupdate='CASCADE')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sleep_param = db.Column(db.SmallInteger(3))
    num_likes = db.Column(db.SmallInteger)
    num_users = db.Column(db.Integer)
    competitor_name = db.Column(db.String(50))
    competitor_id = db.Column(db.BigInteger, index=True)
    working = db.Column(db.SmallInteger(2), default=WORKING_FALSE)


class UnsubscribeCompetitorJob(db.Model):

    id = db.Column(db.Integer, primary_key=True)
