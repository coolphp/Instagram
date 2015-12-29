# coding: utf-8
import os
CSRF_ENABLED = True
SECRET_KEY = 'ksdlldsfnjkdw8er^(&&*@*jdsav2329sadl1'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/insta'

SMTP_USER = 'khigor777@mail.ru'
SMTP_PASSWORD = '545106igor'
SMTP_SERVER = 'smtp.mail.ru'
SMTP_MSG = u'Подвтердите регистрацию на сайте FUNINSTA.RU перейдя по ссылке: '
SMTP_NOTIFICATION_TO = 'khigor777@yandex.ru'