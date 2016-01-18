# coding: utf-8
import os
CSRF_ENABLED = True
SECRET_KEY = 'ksdlldsfnjkdw8er^(&&*@*jdsav2329sadl1'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://root:5tgbfghG%@localhost/insta' #5tgbfghG%
SQLALCHEMY_TRACK_MODIFICATIONS=True

SMTP_USER = 'test@funinsta.ru'#'khigor777@mail.ru'
SMTP_PASSWORD = 'test'#'hfcrhenrfltkf'
SMTP_SERVER = '37.46.128.121'#'smtp.mail.ru'
SMTP_MSG = u'Подтвердите регистрацию на сайте FUNINSTA.RU перейдя по ссылке: '
SMTP_NOTIFICATION_TO = u'khigor777@yandex.ru'