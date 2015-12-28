# coding:utf-8


from flask.ext.wtf import Form
from wtforms import *
from wtforms.validators import DataRequired


class IndexRegisterForm(Form):

    name = StringField('name', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])

