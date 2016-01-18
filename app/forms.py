# coding:utf-8

from wtforms import StringField, TextAreaField, SelectField, IntegerField, HiddenField, RadioField
from wtforms.validators import *
from flask.ext.wtf import Form
from models import *
from wtforms.validators import ValidationError
from api import *


sleep_param = [(unicode(30), 30), (unicode(40), 40), (unicode(50), 50)]

class IndexRegisterForm(Form):

    name = StringField('name', validators=[DataRequired(message=u"Введите данные")])
    phone = StringField('phone')
    whatsapp = StringField('whatsapp')
    email = StringField('email', validators=[DataRequired(message=u"Введите данные"), Email(message=u"Введите Email")])
    instalink = StringField('instalink', validators=[DataRequired(message=u"Введите данные"), URL(message=u"Введите правильный URL")])
    skype = StringField('skype')
    comment = TextAreaField('comment')


class LoginForm(Form):

    user = StringField('user', validators=[DataRequired(message=u"Введите данные")])
    password = StringField('password', validators=[DataRequired(message=u"Введите данные")])


class AddInstaUserForm(Form):
    login = StringField('login', validators=[DataRequired(message=u"Введите данные")])
    password = StringField('password', validators=[DataRequired(message=u"Введите данные")])
    insta_id = IntegerField('insta_id')

    def validate_insta_id(self, field):

        if field.data is False:
            raise ValueError(u'Такого пользователя не существует')

        id = db.session.query(db.func.count(InstaUser.id)).filter_by(insta_id=field.data).scalar()
        if id:
            raise ValidationError(u'Такой пользователь уже существует')

        count = db.session.query(db.func.count(InstaUser.id)).scalar()
        if count > 5:
            raise ValidationError(u'Не более 5 пользователей')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        api = InstagramLikeByTag(self.login.data, self.password.data)
        api = api.is_auth()
        if api is False:
            self.password.errors.append(u'НЕ удалось добавить: Неправильный логин или пароль')
            return False
        return True


class JobLikingForm(Form):
    job_type = HiddenField('job_type', default=Job.TYPE_LIKING_TAG)
    tags = StringField('tags', validators=[DataRequired(message=u"Введите данные")])
    sleep_param = SelectField('sleep_param', choices=sleep_param)
    num_likes = IntegerField('num_likes')
    insta_user_id = SelectField('insta_user_id', validators=[DataRequired(message=u"Введите данные")])


class JobLikingCompetitorForm(Form):
    competitor_name = StringField('competitor_name')
    competitor_id = IntegerField('competitor_id')
    job_type = HiddenField('job_type', default=Job.TYPE_LIKING_COMPETITOR)
    sleep_param = SelectField('sleep_param', choices=sleep_param)
    num_likes = SelectField('num_likes', choices=[(u'1', 1), (u'3', 3), (u'5', 5)])
    num_users = IntegerField('num_users')
    insta_user_id = SelectField('insta_user_id', validators=[DataRequired(message=u"Введите данные")])


class SubscriptTagForm(Form):
    job_type = HiddenField('job_type', default=Job.TYPE_SUBSCRIBTION_TAG)
    tags = StringField('tags', validators=[DataRequired(message=u"Введите данные")])
    sleep_param = SelectField('sleep_param', choices=sleep_param)
    num_likes = SelectField('num_likes', choices=[(u'1', 1), (u'3', 3), (u'5', 5)])
    num_users = IntegerField('num_users')
    insta_user_id = SelectField('insta_user_id', validators=[DataRequired(message=u"Введите данные")])


class SubscriptCompetitor(JobLikingCompetitorForm):
    job_type = HiddenField('job_type', default=Job.TYPE_SUBSCRIBTION_COMPETITOR)


class PayForm(Form):
    bill = RadioField('bill', choices=[(Bills.BILL_FREE, u'Бесплатно 3 дня'),
                                       (Bills.BILL_30_DAYS, u' На 30 дней '+str(Bills.SUM_30_DAYS)+u'руб.'),
                                       (Bills.BILL_180_DAYS, u' На 180 дней '+str(Bills.SUM_180_DAYS)+u'руб.'),
                                       (Bills.BILL_365_DAYS, u' На 365 дней '+str(Bills.SUM_365_DAYS)+u'руб.')],
                      default=Bills.BILL_FREE
                      )

