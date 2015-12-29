# coding: utf-8

import smtplib
from smtplib import SMTPException
from app import app
import logging

logging.basicConfig(filename='smtp_log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Email(object):

    def __init__(self):
        try:
            self.__smtp_login()
        except SMTPException as e:
            logging.debug(e.message)

    def __smtp_login(self):
        with app.app_context():
            server = app.config.get('SMTP_SERVER')
            name = app.config.get('SMTP_USER')
            pwd = app.config.get('SMTP_PASSWORD')
            smtp = smtplib.SMTP_SSL(server)
            smtp.login(name,pwd)
            self.smtp = smtp

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
            with app.app_context():
                from_user = app.config.get('SMTP_USER')
                self.smtp.sendmail(from_user, to, msg)
                self.smtp.quit()
        except SMTPException as e:
            logging.debug(e.message)
