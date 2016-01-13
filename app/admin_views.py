# coding:utf-8

from flask import render_template, redirect, Blueprint, request, url_for, session, flash
from app.forms import *
from models import *
from api import *
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__)


@admin.context_processor
def context_proc():
    def format_working(data):
        if data == Job.WORKING_TRUE:
            return u'В работе'
        return u'Ожидает очереди'

    def format_job_type(data):
        if data == Job.TYPE_SUBSCRIBTION_TAG:
            return u'Подписка по тегам'
        elif (data == Job.TYPE_SUBSCRIBTION_COMPETITOR):
            return u'Подписка по конкурентам'
        return ''

    def format_none(data):
        if data is None:
            return ''
        return data

    return dict(format_working=format_working, format_job_type=format_job_type, format_none=format_none)


@admin.route('/admin/')
@admin.route('/admin/index')
def index():
    session['user_id'] = 1
    return render_template('/admin/index.html')


@admin.route('/admin/adduser/', methods=['GET', 'POST'])
def adduser():
    form = AddInstaUserForm()

    if request.method == 'POST':
        insta_id = InstagramLikeByTag.get_user_id(request.form['login'])
        form = AddInstaUserForm(request.form)
        form.insta_id.data = insta_id
        if form.validate_on_submit():
            add_user(insta_id)

    return render_template('/admin/adduser.html', form=form, users=get_users())


@admin.route('/admin/taglike/', methods=['GET', 'POST'])
def taglike():
    form = JobLikingForm()
    form = set_users(form)
    return render_template('/admin/taglike.html', form=form, jobs=get_tag_like_jobs(Job.TYPE_LIKING_TAG))


@admin.route('/admin/taglike/add', methods=['POST'])
def addtaglike():
    form = JobLikingForm(request.form)
    form = set_users(form)
    if form.validate_on_submit():
        add_job()
        return redirect(url_for('admin.taglike'))
    flash_errors(form)
    return redirect(url_for('admin.taglike'))


@admin.route('/admin/competitor')
def competitor_like():
    form = JobLikingCompetitorForm()
    form = set_users(form)
    return render_template('/admin/competitor_like.html', form=form, jobs=get_tag_like_jobs(Job.TYPE_LIKING_COMPETITOR))


@admin.route('/admin/competitor/add', methods=['POST'])
def add_competitor_like():
    form = JobLikingCompetitorForm(request.form)
    form = set_users(form)
    if form.validate_on_submit():
        add_job_competitor_like()
        return redirect(url_for('admin.competitor_like'))
    flash_errors(form)
    return redirect(url_for('admin.competitor_like'))


@admin.route('/admin/subscript_tags')
def subscript_tags():
    form = SubscriptTagForm()
    form = set_users(form)
    jobs = get_tag_like_jobs(Job.TYPE_SUBSCRIBTION_TAG)
    return render_template('/admin/subscript_tag.html', form=form, jobs=jobs)


@admin.route('/admin/subscript_tags', methods=['POST'])
def add_subscript_tags():
    form = SubscriptTagForm()
    form = set_users(form)
    if form.validate_on_submit():
        add_job_subscript_tag()
        return redirect(url_for('admin.subscript_tags'))
    flash_errors(form)
    return redirect(url_for('admin.subscript_tags'))


@admin.route('/admin/subscript_competitor')
def subscript_competitor():
    form = SubscriptCompetitor()
    form = set_users(form)
    jobs = get_tag_like_jobs(Job.TYPE_SUBSCRIBTION_COMPETITOR)
    return render_template('/admin/subscript_competitor.html', form=form, jobs=jobs)


@admin.route('/admin/add_subscript_competitor', methods=['POST'])
def add_subscript_competitor():
    form = SubscriptCompetitor()
    form = set_users(form)
    if form.validate_on_submit():
        add_job_competitor_like()
        return redirect(url_for('admin.subscript_competitor'))
    flash_errors(form)
    return redirect(url_for('admin.subscript_competitor'))


@admin.route('/admin/unsubcribe')
def unsubcribe():
    subs = db.session.query(Job, User, InstaUser).outerjoin(InstaUser, Job.insta_user_id == InstaUser.id) \
        .outerjoin(User, User.id == InstaUser.user_id).filter(User.id == session['user_id']) \
        .filter((Job.job_type == Job.TYPE_SUBSCRIBTION_COMPETITOR) | (Job.job_type == Job.TYPE_SUBSCRIBTION_TAG)). \
        order_by(Job.job_type).all()
    return render_template('/admin/unsubscript.html', jobs=subs)



@admin.route('/admin/blank/')
def blank():
    return render_template('/admin/blank.html')


def set_users(form):
    users = get_users()
    users = [(unicode(x.id), x.login) for x in users]
    form.insta_user_id.choices = users
    return form


def add_job():
    job = Job(insta_user_id=request.form['insta_user_id'],
              job_type=request.form['job_type'],
              sleep_param=request.form['sleep_param'],
              tags=request.form['tags'],
              num_likes=request.form['num_likes']
              )
    db.session.add(job)
    db.session.commit()


def add_job_competitor_like():
    inst_id = InstagramLikeByTag.get_user_id(request.form['competitor_name'])

    job = Job(insta_user_id=request.form['insta_user_id'],
              job_type=request.form['job_type'],
              sleep_param=request.form['sleep_param'],
              num_likes=request.form['num_likes'],
              num_users=request.form['num_users'],
              competitor_id=inst_id,
              competitor_name=request.form['competitor_name']
              )
    db.session.add(job)
    db.session.commit()


def add_job_subscript_tag():
    print(request.form)
    job = Job(insta_user_id=request.form['insta_user_id'],
              job_type=request.form['job_type'],
              sleep_param=request.form['sleep_param'],
              tags=request.form['tags'],
              num_likes=request.form['num_likes'],
              num_users=request.form['num_users']
              )
    db.session.add(job)
    db.session.commit()


def get_tag_like_jobs(type):
    return db.session.query(Job, User, InstaUser).outerjoin(InstaUser, Job.insta_user_id == InstaUser.id) \
        .outerjoin(User, User.id == InstaUser.user_id).filter(User.id == session['user_id']) \
        .filter(Job.job_type == type).all()


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
