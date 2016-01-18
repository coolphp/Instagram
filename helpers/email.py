# -*- coding: UTF-8 -*-

import smtplib
from smtplib import SMTPException
from app import app
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#filename='smtp_log.log',

class Email(object):

    def __init__(self):
        try:
            self.smtp_login()
        except SMTPException as e:
            logging.debug(e.args)

    def smtp_login(self):
        server = app.config.get('SMTP_SERVER')
        name = app.config.get('SMTP_USER')
        pwd = app.config.get('SMTP_PASSWORD')
        smtp = smtplib.SMTP_SSL(server)
        self.smtp = smtp
        return self.smtp.login(name, pwd)



    def send_notify_auth(self, to, auth_link):
        """
        Send message to with_auth_link
        :param to:
        :param auth_link:
        :return:
        """
        msg = app.config.get('SMTP_MSG')+auth_link
        return self.send_message(to, unicode(msg))

    def send_message(self, to, msg):
        try:
            from_user = app.config.get('SMTP_USER')
            msg = msg.encode('utf-8', 'ignore')
            res = self.smtp.sendmail(from_user, to, msg)
            self.smtp.quit()
        except SMTPException as e:
            logging.debug(e.args)
            return e.args
        return res
