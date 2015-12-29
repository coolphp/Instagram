# coding:utf-8
from app import app
from flask import render_template, flash, redirect, request, url_for
from app.forms import IndexRegisterForm
from app import db, models
import uuid
from helpers.email import Email



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = IndexRegisterForm()
    if form.validate_on_submit():
        data = request.form

        u = models.User(name=data['name'], phone=data['phone'],
                        whatsapp=data['whatsapp'], email = data['email'],
                        instalink = data['instalink'], skype=data['skype'],
                        comment = data['comment'])

        db.session.add(u)
        db.session.commit()
        hash_e = uuid.uuid4()
        email_confirm = models.EmailConfirmation(user_id=u.id, hash_confirm=hash_e)
        db.session.add(email_confirm)
        db.session.commit()

        send_email(data)
        send_email_conformation(data, hash_e)

        return redirect(url_for('success'))

    flash_errors(form)
    return render_template('index.html', form=form)

@app.route('/success')
def success():
    return render_template('success.htm')

app.route('/confirm_email/<str:hash_email>')
def confirm_email(hash_email):
    email = models.EmailConfirmation.query.filter_by(hash_confirm=hash_email).first()
    u_id = email.user_id
    u = models.User.query.filter_by(id=u_id).first()
    u.confirmation = models.User.CONFIRMATION_TRUE
    db.session.add(u)
    db.session.commit()


def send_email(data):
    email = Email()
    res = u'Запрос с сайта: '+"\n\r"
    for k, v in data.iteritems():
        res+=u"{} : {} \n\r".format(k, v)
    email.send_message(app.config.get('SMTP_NOTIFICATION_TO'),res)

def send_email_conformation(data, hash_e):
    url = url_for('confirm_email',hash_email=hash_e)
    email = Email()
    email.send_notify_auth(data['email'], url)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Ошибка в %s - %s" % (
                getattr(form, field).label.text,
                error
            ))

