# coding:utf-8

from flask import render_template, flash, redirect, Blueprint
admin = Blueprint('admin', __name__)

@admin.route('/admin/')
def index():
    return render_template('/admin/index.html')

@admin.route('/admin/form/')
def form():
    return render_template('/admin/form.html')
