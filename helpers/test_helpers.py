# coding: utf-8
import pytest


class TestEmail(object):
    AUTH_SUCCESS = 235
    NOTIFY_EMAIL = 'test@test.ru'

    @pytest.fixture(scope="session")
    def set_up(self):
        from helpers.email import Email
        return Email()

    def test_smtp_login(self):
        email = self.set_up()
        code, msg = email.smtp_login()
        assert code == self.AUTH_SUCCESS

    def test_send_notify_auth(self):
        email = self.set_up()
        res = email.send_notify_auth(self.NOTIFY_EMAIL, auth_link='test_link')
        assert len(res) == 0


    def test_send_message(self):
        email = self.set_up()
        res = email.send_message(self.NOTIFY_EMAIL, 'test_msg')
        assert len(res) == 0
