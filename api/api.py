# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from lxml import html
import selenium.common.exceptions
import requests
import urlparse
import json
import re

class InstagramApi(object):

    __access_token = None
    client_id = '58acc6be0e5249658699556b8a7a3f4d'
    secret='78c1c0ac22b94cc78506983687fecea0'
    user_id = None
    user_login = 'khigor777'
    user_password = '545106igor'

    def __init__(self):
        self.browser = webdriver.Firefox()
        self.set_access_token()
        self.set_user_id()

    def set_access_token(self):
        self.browser.get('https://api.instagram.com/oauth/authorize/?client_id={}&redirect_uri={}&response_type=code&scope={}'.
                         format(self.client_id, 'http://ya.ru', 'follower_list'))

        time.sleep(1)
        self.auth()
        time.sleep(1)
        code = urlparse.urlparse(self.browser.current_url)
        code = urlparse.parse_qs(code.query)['code']
        params = {
            'client_id': self.client_id,
            'client_secret': self.secret,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://ya.ru',
            'code': code

        }
        r = requests.post('https://api.instagram.com/oauth/access_token', params)
        self.__access_token = json.loads(r.content)['access_token']

    def auth(self):
        input_name = self.browser.find_element_by_name('username')
        input_name.send_keys(self.user_login)
        input_password = self.browser.find_element_by_name('password')
        input_password.send_keys(self.user_password)
        submit = self.browser.find_element_by_class_name('button-green')
        submit.click()
        time.sleep(2)
        try:
            btn = self.browser.find_element_by_xpath('//input[@value="Authorize"]')
            btn.click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def set_user_id(self, user_login='khigor777'):
        url = 'https://www.instagram.com/{}/'.format(user_login)
        r = requests.get(url)
        r = re.search('"id":"(.*?)"', r.content)
        try:
            self.user_id = r.group(1)
        except AttributeError:
            self.user_id = 0
            return self.user_id
        return self.user_id

    def get_followed_users(self):
        r = requests.get('https://api.instagram.com/v1/users/{}/followed-by?access_token={}'.format(self.user_id, self.__access_token))
        print(r.content)

#api = InstagramApi()
#api.set_user_id('khigor777')
#api.get_followed_users()
