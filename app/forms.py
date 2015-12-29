# coding:utf-8

from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, URL, Email
from flask.ext.wtf import Form


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

