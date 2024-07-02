import traceback

from app import create_app
from app import config_data
from app import logger
from flask import render_template
from flask_mail import Mail
from flask_mail import Message

app,mail=create_app()
app.config['MAIL_SERVER'] = config_data['MAIL']['MAIL_SERVER']
app.config['MAIL_PORT'] = config_data['MAIL']['MAIL_PORT']
app.config['MAIL_USERNAME'] = config_data['MAIL']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config_data['MAIL']['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config_data['MAIL']['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config_data['MAIL']['MAIL_USE_SSL']
# app.config['MAIL_DEFAULT_SENDER'] = config_data['MAIL']['MAIL_DEFAULT_SENDER']
# app.config['MAIL_DEFAULT_SENDER'] = 'mailtrap@demomailtrap.com'

# app.config['MAIL_DEBUG'] = True
# app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'api'
# app.config['MAIL_PASSWORD'] = '189250e6a4bdc77539df63cc6d5f14f9'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


def send_mail(email_to, subject, template, data={}):
    """This method is used to send emails."""
    try:

        msg = Message(subject, sender=config_data['MAIL']['MAIL_DEFAULT_SENDER'], recipients=[email_to])

        with app.app_context():
            msg.html = render_template(template, **data)

            mail.send(msg)
            logger.info(f'Mail sent successfully to: {email_to}')
            
        
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error('Unable to send mail: ' + str(e))
        print(traceback.format_exc())