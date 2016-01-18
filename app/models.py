# coding: utf-8
from app import db
import datetime


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
    user_role = db.Column(db.SmallInteger, default=ROLE_USER)
    password = db.Column(db.String(20))
    confirmation = db.Column(db.SmallInteger, default=CONFIRMATION_FALSE)
    EmailConfirmation = db.relationship('EmailConfirmation', backref=db.backref('conf'), lazy='dynamic')
    bill_type = db.Column(db.SmallInteger)


class Bills(db.Model):
    BILL_FREE = unicode(0)
    BILL_30_DAYS = unicode(1)
    BILL_180_DAYS = unicode(2)
    BILL_365_DAYS = unicode(3)

    SUM_FREE = unicode(0)
    SUM_30_DAYS = unicode(590)
    SUM_180_DAYS = unicode(3186)
    SUM_365_DAYS = unicode(5664)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", onupdate='CASCADE'))
    bill_type = db.Column(db.SmallInteger, default=BILL_FREE)
    pay_begin = db.Column(db.DATETIME, default=datetime.datetime.now())
    pay_finish = db.Column(db.DATETIME)
    bill_sum = db.Column(db.Float, default=SUM_FREE)

    @staticmethod
    def get_days(bill_type):
        days = {Bills.BILL_FREE: 3,
                Bills.BILL_30_DAYS: 30,
                Bills.BILL_180_DAYS: 180,
                Bills.BILL_365_DAYS: 365
                }

        if bill_type in days:
            return days[bill_type]
        raise Exception(u'Нет такого счета')

    @staticmethod
    def get_date_finish(bill_type, now):
        days = Bills.get_days(bill_type)
        date_finish = now + datetime.timedelta(days=days)
        return date_finish

    @staticmethod
    def get_sum_from_bill(bill_type):
        sum = {Bills.BILL_FREE: Bills.SUM_FREE,
               Bills.BILL_30_DAYS: Bills.SUM_30_DAYS,
               Bills.BILL_180_DAYS: Bills.SUM_180_DAYS,
               Bills.BILL_365_DAYS: Bills.SUM_365_DAYS
               }
        if bill_type in sum:
            return sum[bill_type]
        raise Exception(u'Нет такой суммы')


class EmailConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", onupdate='CASCADE'))
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
    job_type = db.Column(db.SmallInteger, default='NULL')
    sleep_param = db.Column(db.SmallInteger)
    num_likes = db.Column(db.SmallInteger)
    num_users = db.Column(db.Integer)
    competitor_name = db.Column(db.String(50))
    tags = db.Column(db.String(150))
    competitor_id = db.Column(db.BigInteger, index=True)
    working = db.Column(db.SmallInteger, default=WORKING_FALSE)
    working_start = db.Column(db.DATETIME, default=datetime.datetime.now())


class Log(db.Model):
    SUBSCRIBE = 0
    UN_SUBSCRIBE = 1

    id = db.Column(db.BigInteger, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete="CASCADE", onupdate='CASCADE'))
    url = db.Column(db.String(200))
    event_time = db.Column(db.DATETIME, default=datetime.datetime.now())
    un_subcribe = db.Column(db.SmallInteger, default=SUBSCRIBE)


class Subscription(db.Model):
    IS_PRIVATE_TRUE = 0
    IS_PRIVATE_FALSE = 1

    id = db.Column(db.BigInteger, primary_key=True)
    insta_name = db.Column(db.String(200))

    followed_id = db.Column(db.BigInteger)
    followed_name = db.Column(db.String(200))
    is_private = db.Column(db.SmallInteger, default=IS_PRIVATE_TRUE)
    profile_pic_url = db.Column(db.String(500))
    full_name = db.Column(db.String(250))

    @staticmethod
    def add_subscribers(insta_name, item):

        for data in item:
            sub = Subscription(insta_name=insta_name,
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
        if unicode(data) == u'False':
            return Subscription.IS_PRIVATE_FALSE
        return Subscription.IS_PRIVATE_TRUE
