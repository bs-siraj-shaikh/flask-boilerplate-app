"""Contains methods and logic to send emails."""
import traceback

from app import config_data
from app import create_app
from app import logger
from flask import render_template
from tasks import send_background_email
# from providers.mail import send_mail
# from tasks import


app, mail = create_app()
app.config['MAIL_SERVER'] = config_data['MAIL']['MAIL_SERVER']
app.config['MAIL_PORT'] = config_data['MAIL']['MAIL_PORT']
app.config['MAIL_USERNAME'] = config_data['MAIL']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config_data['MAIL']['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config_data['MAIL']['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config_data['MAIL']['MAIL_USE_SSL']


class EmailWorker:
    """This worker contains different methods for sending email."""
    @classmethod
    def send(cls, data):
        """This method is used for sending emails."""
        try:
            with app.app_context():
                email_to = data.get('email_to', None)  # type: ignore  # noqa: FKA100
                subject = data.get('subject', None)  # type: ignore  # noqa: FKA100
                template = data.get('template', None)  # type: ignore  # noqa: FKA100
                # email_type = data.get('email_type', None)  # type: ignore  # noqa: FKA100
                email_data = data.get('email_data', None)  # type: ignore  # noqa: FKA100
                # org_id = data.get('org_id', None)  # type: ignore  # noqa: FKA100
                logger.info('sent mail')
                html_body = render_template(template, **email_data)

                send_background_email.delay(subject=subject, sender=config_data['MAIL']['MAIL_DEFAULT_SENDER'], recipients=[
                                            email_to], html_body=html_body)
        except Exception as e:
            logger.error(
                'Inside EmailWorker.send() : ' + str(e))
            logger.error(traceback.format_exc())
