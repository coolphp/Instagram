# coding: utf-8
from app import db
import datetime
from api.main import Instagram


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
    user_id=db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", onupdate='CASCADE'))
    hash_confirm = db.Column(db.String(100))


class InstaUser(db.Model):

    __tablename__ = 'instauser'


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))
    insta_id = db.Column(db.BigInteger, unique=True)


class Job(db.Model):

    # WORKING TYPES
    WORKING_FALSE = 0
    WORKING_TRUE = 1

    # JOB TYPES
    TYPE_LIKING_TAG = 0
    TYPE_LIKING_COMPETITOR = 1
    TYPE_SUBSCRIBTION_TAG = 2
    TYPE_SUBSCRIBTION_COMPETITOR = 3
    TYPE_UNSUBSCRIBTION = 4

    id = db.Column(db.Integer, primary_key=True)
    insta_user_id = db.Column(db.Integer, db.ForeignKey('instauser.id', ondelete="CASCADE", onupdate='CASCADE'))
    job_type = db.Column(db.SmallInteger(3), default='NULL')
    sleep_param = db.Column(db.SmallInteger(3))
    num_likes = db.Column(db.SmallInteger)
    num_users = db.Column(db.Integer)
    competitor_name = db.Column(db.String(50))
    tags = db.Column(db.String(150))
    competitor_id = db.Column(db.BigInteger, index=True)
    working = db.Column(db.SmallInteger(2), default=WORKING_FALSE)
    working_start = db.Column(db.DATETIME, default=datetime.datetime.now())


class Log(db.Model):

    id = db.Column(db.BigInteger, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete="CASCADE", onupdate='CASCADE'))
    url = db.Column(db.String(200))
    event_time = db.Column(db.DATETIME, default=datetime.datetime.now())


class Subscription(db.Model):

    IS_PRIVATE_TRUE = 0
    IS_PRIVATE_FALSE = 1

    id = db.Column(db.BigInteger, primary_key=True)
    insta_name = db.Column(db.String(200))
    insta_id = db.Column(db.BigInteger)

    followed_id = db.Column(db.BigInteger)
    followed_name = db.Column(db.String(200))
    is_private = db.Column(db.SmallInteger(2), default=IS_PRIVATE_TRUE)
    profile_pic_url = db.Column(db.String(500))
    full_name = db.Column(db.String(250))

    @staticmethod
    def add_subscribers(insta_id, item):
        insta_user = db.session.query(InstaUser).filter_by(id=insta_id).one()
        user_id = Instagram.get_user_id(insta_user.login)

        for data in item:
            sub = Subscription(insta_name=insta_user.login,
                               insta_id=user_id,
                               followed_id=data['pk'],
                               followed_name=data['username'],
                               is_private=Subscription.get_private_type(data['is_private']),
                               profile_pic_url=data['profile_pic_url'],
                               full_name=data['full_name']
                               )
            db.session.add(sub)
        db.session.commit()

    @staticmethod
    def get_private_type(data):
        IS_PRIVATE_TRUE = 0
        IS_PRIVATE_FALSE = 1
        if data == 'False':
            return IS_PRIVATE_FALSE
        return IS_PRIVATE_TRUE



