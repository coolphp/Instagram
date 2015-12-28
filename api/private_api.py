# coding: utf-8
import requests
import json
import re
import time

'''
    #api = InstagramPrivateApi()
    #api.set_user_login('khigor777')
    #print(api.get_followed())
'''
class InstagramPrivateApi(object):

    def __init__(self):
        self.session = requests.Session()
        self.user_id = 0
        self.user_login = 'khigor777'
        self.url = 'https://i.instagram.com/api/v1/'

    def get_followed(self):
        url = self.url + 'friendships/{}/followers/'.format(self.user_id)
        res = self.request(url)
        result = res['users']

        while True:
            if 'next_max_id' not in res:
                break
            max_id = res['next_max_id']
            url = self.url + 'friendships/{}/followers/?max_id={}'.format(self.user_id, max_id)
            res = self.request(url)
            for i in res['users']:
                result.append(i.copy())
            time.sleep(2)
        return result


    def request(self, url):
        res = self.session.get(url)
        res = json.loads(res.content)
        return res


    def __set_user_id(self):
        url = 'https://www.instagram.com/{}/'.format(self.user_login)
        r = requests.get(url)
        r = re.search('"id":"(.*?)"', r.content)
        try:
            self.user_id = r.group(1)
        except AttributeError:
            self.user_id = 0
            return self.user_id
        return self.user_id

    def set_user_login(self, user_login):
        self.user_login = user_login
        self.__set_user_id()


