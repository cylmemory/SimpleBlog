from threading import Thread
from .. import mail
from flask_mail import Message
from flask import current_app, render_template


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template_txt, template_html=None, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject)
    msg.sender = current_app._get_current_object().config['MAIL_USERNAME']
    msg.recipients = [to]

    if not template_html:
        template_html = template_txt
    msg.body = render_template(template_txt, **kwargs)
    msg.html = render_template(template_html, **kwargs)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_confirm_email(to, user, token):
    title = 'Simple Blog confirm user email'
    template_txt = 'useraccounts/email/confirm.txt'
    template_html = 'useraccounts/email/confirm.html'

    return send_email(to, title, template_txt, template_html, user=user, token=token)


def send_reset_password_mail(to, user, token):
    title = 'Simple Blog reset user password'
    template_txt = 'useraccounts/email/reset_password.txt'
    template_html = 'useraccounts/email/reset_password.html'

    return send_email(to, title, template_txt, template_html, user=user, token=token)
