# coding: utf-8
from app.models import *
import hashlib


class Robokassa(object):
    MERCHANT_LOGIN = 'instabiz'
    SECRET_KEY_FIRST = 'N6Km2MRM1Ih4tg9LXnEQ'
    SECRET_KEY_SECOND = 'nJ0O1g23Hifdi5fMdwHv'
    TEST_SECRET_KEY_FIRST = 'zE9KbUkpD5e6Payzs4X3'
    TEST_SECRET_KEY_SECOND = 'c3JgPffkcjr6Eqh8Bu91'
    URL = 'https://auth.robokassa.ru/Merchant/Index.aspx?'


    def insert_bill(self, user_id, bill_type):
        bill = Bills(
            user_id=user_id,
            bill_type=bill_type,
            bill_sum=Bills.get_sum_from_bill(bill_type))
        db.session.add(bill)
        db.session.commit()
        return bill

    def update_bill(self, bill_id):
        now = datetime.datetime.now()
        bill = Bills.query.get(bill_id)
        bill.pay_begin = now
        bill.pay_finish = Bills.get_date_finish(bill.bill_type, now)
        db.session.commit()
        return bill


    def getUrlForBill(self, bill):
        sum = int(bill.bill_sum)
        inv_id = bill.id
        src = hashlib.md5('{}:{}:{}:{}'.format(self.MERCHANT_LOGIN, sum, inv_id, self.TEST_SECRET_KEY_FIRST)).hexdigest()
        params = {
            'MerchantLogin': self.MERCHANT_LOGIN,
            'OutSum': sum,
            'InvId': inv_id,
            'Desc': 'Instagram',
            'SignatureValue': src,
            'IsTest': 1
        }
        return self.URL + '&'.join(['{}={}'.format(k, v) for k, v in params.items()])

    def check_payment_result(self, value):
        self._check(value, self.TEST_SECRET_KEY_SECOND)

    def check_payment_success(self, value):
        self._check(value, self.TEST_SECRET_KEY_FIRST)

    def _check(self, value, key):
        out_summ = value["OutSum"]
        inv_id = value["InvId"]
        crc = value["SignatureValue"]
        src = hashlib.md5('{}:{}:{}'.format(out_summ, int(inv_id), key)).hexdigest()
        if crc.upper() == src.upper():
            return True
        return False
