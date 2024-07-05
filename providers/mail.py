import traceback

from app import config_data
from app import create_app
from app import logger
from flask import render_template
from flask_mail import Mail
from flask_mail import Message
# from threading import Thread
# from tasks import send_background_email


app, mail = create_app()
app.config['MAIL_SERVER'] = config_data['MAIL']['MAIL_SERVER']
app.config['MAIL_PORT'] = config_data['MAIL']['MAIL_PORT']
app.config['MAIL_USERNAME'] = config_data['MAIL']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config_data['MAIL']['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config_data['MAIL']['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config_data['MAIL']['MAIL_USE_SSL']

mail = Mail(app)


def send_mail(email_to, subject, template, data):
    """This method is used to send emails."""
    try:

        msg = Message(
            subject, sender=config_data['MAIL']['MAIL_DEFAULT_SENDER'], recipients=[email_to])
        msg.html = render_template(template, **data)
        mail.send(msg)
        logger.info(f'Mail sent successfully to: {email_to}')
        # with app.app_context():

        # html_body = render_template(template, **data)
        # send_background_email.delay(subject,sender=config_data['MAIL']['MAIL_DEFAULT_SENDER'],recipients=[email_to],html_body=html_body)

        # mail.send(msg)
        # thr=Thread(target=send_mail_thread,args=[msg])
        # thr.start()
        # logger.info(f'Mail sent successfully to: {email_to}')

    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error('Unable to send mail: ' + str(e))
