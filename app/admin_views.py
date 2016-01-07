# coding:utf-8

from flask import render_template, redirect, Blueprint, request, url_for, session, flash
from app.forms import *
from models import *
from api.main import Instagram
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__)

@admin.context_processor
def context_proc():

    def format_working(data):
        if data == Job.WORKING_TRUE:
            return u'В работе'
        return u'Ожидает очереди'
    return dict(format_working=format_working)


@admin.route('/admin/')
@admin.route('/admin/index')
def index():
    session['user_id'] = 1
    return render_template('/admin/index.html')


@admin.route('/admin/adduser/', methods=['GET', 'POST'])
def adduser():
    form = AddInstaUserForm()

    if request.method == 'POST':
        insta_id = Instagram.get_user_id(request.form['login'])
        form = AddInstaUserForm(request.form)
        form.insta_id.data = insta_id
        if form.validate_on_submit():
            add_user(insta_id)

    return render_template('/admin/adduser.html', form=form, users=get_users())


@admin.route('/admin/taglike/', methods=['GET', 'POST'])
def taglike():
    print(get_tag_like_jobs())
    form = JobLikingForm()
    users = get_users()
    users = [(x.id, x.login) for x in users]
    form.insta_user_id.choices = users
    return render_template('/admin/taglike.html', form=form, jobs=get_tag_like_jobs())


@admin.route('/admin/taglike/add', methods=['POST'])
def addtaglike():
    form = JobLikingForm(request.form)
    users = get_users()
    users = [(unicode(x.id), x.login) for x in users]
    form.insta_user_id.choices = users
    print(users, request.form)
    if form.validate_on_submit():
        add_job()
        return redirect(url_for('admin.taglike'))
    flash_errors(form)
    return redirect(url_for('admin.taglike'))





@admin.route('/admin/blank/')
def blank():
    return render_template('/admin/blank.html')


def add_job():
    job = Job(insta_user_id=request.form['insta_user_id'],
              job_type=request.form['job_type'],
              sleep_param=request.form['sleep_param'],
              tags=request.form['tags'],
              num_likes=request.form['num_likes']
              )
    db.session.add(job)
    db.session.commit()


def get_tag_like_jobs():
    return db.session.query(Job, User, InstaUser).outerjoin(InstaUser, Job.insta_user_id == InstaUser.id)\
            .outerjoin(User, User.id == InstaUser.user_id).filter(User.id == session['user_id'])\
            .filter(Job.job_type == Job.TYPE_LIKING_TAG).all()

def get_users():
    return db.session.query(InstaUser).filter_by(user_id=session['user_id']).all()


def add_user(insta_id):
    user = InstaUser(login=request.form['login'],
                     password=request.form['password'],
                     user_id=session['user_id'],
                     insta_id=insta_id
                     )
    db.session.add(user)
    db.session.commit()


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Ошибка в %s - %s" % (
                getattr(form, field).label.text,
                error
            ))
