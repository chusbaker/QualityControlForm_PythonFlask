from flask_mail import Message
from flask import render_template
from threading import Thread
import os

from app import app, mail
from app.routes import data

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    Thread(target=send_async_email, args=(app, msg)).start()

def send_records_email():
    user = os.getenv('username')
    u_mail = user + "gmail.com"

    send_email('A new [QCForm] has been received',
               sender=app.config['ADMINS'][0],
               recipients=[u_mail],
               text_body=repr(data),
               html_body=repr(data))

