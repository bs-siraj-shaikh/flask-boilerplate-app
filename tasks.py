# tasks.py
""" Returns gmail in background using celery and redis"""
from app import config_data
from celery import Celery
from flask import Flask
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = config_data['CELERY_BROKER_URL']
app.config['CELERY_RESULT_BACKEND'] = config_data['CELERY_RESULT_BACKEND']

app.config['MAIL_SERVER'] = config_data['MAIL']['MAIL_SERVER']
app.config['MAIL_PORT'] = config_data['MAIL']['MAIL_PORT']
app.config['MAIL_USERNAME'] = config_data['MAIL']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config_data['MAIL']['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config_data['MAIL']['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config_data['MAIL']['MAIL_USE_SSL']


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


mail = Mail(app)


@celery.task
def send_background_email(subject, sender, recipients, html_body):
    """ return gmail with msg"""

    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.html = html_body

    with app.app_context():
        mail.send(msg)
