# coding: utf-8

import smtplib
from smtplib import SMTPException
from app import app
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#filename='smtp_log.log',

class Email(object):

    def __init__(self):
        try:
            self.__smtp_login()
        except SMTPException as e:
            logging.debug(e.args)

    def __smtp_login(self):
        server = app.config.get('SMTP_SERVER')
        name = app.config.get('SMTP_USER')
        pwd = app.config.get('SMTP_PASSWORD')
        smtp = smtplib.SMTP_SSL(server)
        self.smtp = smtp
        self.smtp.login(name, pwd)



    def send_notify_auth(self, to, auth_link):
        """
        Send message to with_auth_link
        :param to:
        :param auth_link:
        :return:
        """
        msg = app.config.get('SMTP_MSG')+auth_link
        self.send_message(to, msg)

    def send_message(self, to, msg):
        try:
            from_user = app.config.get('SMTP_USER')
            self.smtp.sendmail(from_user, to, msg)
            self.smtp.quit()
        except SMTPException as e:
            logging.debug(e.args)
