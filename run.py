# coding:utf-8
import pytest
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from app import app
app.run(debug=True, use_reloader=True)
