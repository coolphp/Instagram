# coding: utf-8

from app.models import *
from redis import *
from rq import Queue
from worker import print_l


q = Queue(connection=Redis())
result = q.enqueue(print_l)
print(result)
