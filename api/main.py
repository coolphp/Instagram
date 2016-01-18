# coding: utf-8
from selenium import webdriver
import time
from lxml import html
import selenium.common.exceptions
import requests
import re
from private_api import InstagramPrivateApi
from app.models import *
from selenium.webdriver.common.keys import Keys



class MainClass(object):
    browser = None
    url = 'https://www.instagram.com/'

    def __init__(self, user_name, password):
        self.browser = webdriver.Firefox()
        #self.browser = webdriver.PhantomJS(executable_path='C:\phantomJs\phantomjs.exe')#
        self.user_name = user_name
        self.password = password
        self.auth()

    def auth(self):
        self.browser.get(self.url)
        time.sleep(7)
        try:
            link = self.browser.find_element_by_xpath(u"//a[contains(text(),'Вход')]")
            link.click()
        except Exception:
            pass
        time.sleep(5)
        input_name = self.browser.find_element_by_name('username')
        input_name.send_keys(self.user_name)
        input_password = self.browser.find_element_by_name('password')
        input_password.send_keys(self.password)
        submit = self.browser.find_element_by_tag_name('button')
        submit.click()
        time.sleep(5)

    def is_auth(self):
        try:
            self.browser.find_element_by_link_text(self.user_name)
        except selenium.common.exceptions.NoSuchElementException:
            return False
        return True

    def like(self):
        try:
            like = self.browser.find_element_by_xpath('//body/div[2]/div/div[2]/div/article/div[2]/section[2]/a')
            like.click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def __get_num_of_publucation(self, html_data):
        res = html.fromstring(html_data)
        res = res.xpath('//header/span/span[2]/text()')
        res = res[0].replace(',', '')
        return int(res)

    def find_first_picture_and_click(self):
        first = self.browser.find_element_by_xpath('//main/article/div/div/div/a')
        first.click()
        time.sleep(5)

    def click_next(self):
        next = self.browser.find_element_by_xpath(u"//*[contains(text(),'Далее')]")
        next.click()
        time.sleep(7)

    def goto_tag(self, tag):
        url = self.url + 'explore/tags/{}/'.format(tag)
        self.browser.get(url)
        time.sleep(4)

    def get_num_publication(self):
        return self.__get_num_of_publucation(self.browser.page_source)

    def like_num_times(self, num=3):
        for i in xrange(num):
            self.click_next()
            time.sleep(3)
            self.like()
            time.sleep(10)


    @staticmethod
    def get_user_id(user_login='khigor777'):
        url = 'https://www.instagram.com/{}/'.format(user_login)
        r = requests.get(url)
        r = re.search('"id":"(.*?)"', r.content)
        try:
            user_id = r.group(1)
        except AttributeError:
            return False
        return user_id


class InstagramLikeByTag(MainClass):
    def run(self, tag=u"секс"):
        '''
        Пролайкать по заданным тегам
        :param tag:
        :return:
        '''
        self.goto_tag(tag)
        num = self.get_num_publication()
        self.find_first_picture_and_click()
        time.sleep(7)
        self.like()
        self.like_num_times(num)


class InstagramLikeByCompetitor(MainClass):
    def __init__(self, user_name, password, time_out=30, competitor_name='khigor777'):
        super(InstagramLikeByCompetitor, self).__init__(user_name=user_name, password=password)
        self.timeout = time_out
        self.competitor_name = competitor_name

    def run(self):
        res = self.get_followed()
        for item in res:
            self.browser.get(self.url+item.followed_name)
            self.find_first_picture_and_click()
            time.sleep(5)
            self.like()
            for num in xrange(2):
                self.click_next()
                time.sleep(5)
                self.like()


    def get_followed(self):
        res = self.get_followed_from_db()
        if res:
            return res
        self.set_followed()
        res = self.get_followed_from_db()
        return res

    def set_followed(self):
        api = InstagramPrivateApi()
        api.set_user_login(self.competitor_name)
        followed = api.get_followed()
        Subscription.add_subscribers(self.competitor_name, followed)

    def get_followed_from_db(self):
        return db.session.query(Subscription) \
            .filter(Subscription.insta_name == self.competitor_name) \
            .filter(Subscription.is_private == Subscription.IS_PRIVATE_FALSE) \
            .all()


class SubscriptionByTag(MainClass):
    def __init__(self, user_name, password, tag=u'Москва'):
        super(SubscriptionByTag, self).__init__(user_name=user_name, password=password)
        self.tag = tag

    def goto_user_name(self):
        user = self.browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/article/header/div/a[1]').get_attribute('title')
        print(user)
        self.browser.get(self.url+user)
        time.sleep(5)

    def click_subscript(self):
        sub = self.browser.find_element_by_xpath('html/body/div[2]/div/div[2]/div/article/header/span/button')
        sub.click()
        time.sleep(5)

    def like_user_name(self, first_tab):
        self.browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "t")
        self.goto_user_name()
        self.find_first_picture_and_click()
        self.like()
        self.like_num_times(1)
        self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        self.browser.switch_to.window(first_tab)

    def run(self):
        first_tab = self.browser.current_window_handle
        self.goto_tag(self.tag)
        num = self.get_num_publication()
        self.find_first_picture_and_click()
        for i in xrange(num):
            time.sleep(3)
            self.click_subscript()
            self.click_next()
            self.like_user_name(first_tab)


class SubscriptionByCompetitor(InstagramLikeByCompetitor, SubscriptionByTag):

    def click_subscript(self):
        sub = self.browser.find_element_by_xpath('//section/main/article/header/div[2]/div[1]/span/button')
        sub.click()
        time.sleep(5)



    def run(self):
        res = self.get_followed()
        for item in res:
            self.browser.get(self.url+item.followed_name)
            self.click_subscript()
            self.find_first_picture_and_click()
            time.sleep(5)
            self.like()
            for num in xrange(2):
                self.click_next()
                time.sleep(5)
                self.like()



def like_by_tag():
    inst = InstagramLikeByTag('khigor777', '545106igor')
    inst.run(u'Брянск')

def like_by_competitor():
    inst = InstagramLikeByCompetitor('khigor777', '545106igor', competitor_name='sdemina')
    inst.run()

def subscription_by_tag():
    inst = SubscriptionByTag('khigor777', '545106igor')
    inst.run()

def subscript_by_competitor():
    inst = SubscriptionByCompetitor('khigor777', '545106igor',competitor_name='sdemina')
    inst.run()

if __name__ == '__main__':
    inst = InstagramLikeByTag('khigor777', '545106igor')
    inst.run(u'Брянск')
