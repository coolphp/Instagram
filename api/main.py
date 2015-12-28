# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from lxml import html
import selenium.common.exceptions
import requests
import urlparse
import json


class Instagram(object):
    browser = None
    url = 'https://www.instagram.com/'

    def __init__(self, user_name, password):
        self.browser = webdriver.Firefox()
        # browser = webdriver.PhantomJS(executable_path='C:\phantomJs\phantomjs.exe')#
        self.user_name = user_name
        self.password = password
        self.auth()

    def auth(self):
        self.browser.get(self.url)
        time.sleep(7)
        input_name = self.browser.find_element_by_name('username')
        input_name.send_keys(self.user_name)
        input_password = self.browser.find_element_by_name('password')
        input_password.send_keys(self.password)
        submit = self.browser.find_element_by_tag_name('button')
        submit.click()
        time.sleep(5)

    def like_by_tag(self, tag=u"секс"):
        '''
        Пролайкать по заданным тегам
        :param tag:
        :return:
        '''
        url = self.url + 'explore/tags/{}/'.format(tag)
        self.browser.get(url)
        num = self.get_num_of_publucation(self.browser.page_source)
        first = self.browser.find_element_by_xpath('(//a[@class="t89 g59"])[1]')
        first.click()
        time.sleep(7)
        for i in xrange(num):
            next = self.browser.find_element_by_xpath('//a[@class="v79 coreSpriteRightPaginationArrow"]')
            next.click()
            time.sleep(3)
            self.like()
            time.sleep(10)

    def like(self):
        try:
            like = self.browser.find_element_by_xpath('//a[@class="w59 h99 u77 coreSpriteHeartOpen"]')
            like.click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def get_num_of_publucation(self, html_data):
        res = html.fromstring(html_data)
        res = res.xpath('//span[@class="l39"]/text()')
        res = res[0].replace(',', '')
        return int(res)


if __name__ == '__main__':
    inst = Instagram('khigor777', '545106igor')
    # inst.like_by_tag(u'Брянск')
