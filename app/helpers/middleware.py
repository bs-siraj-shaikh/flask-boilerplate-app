from datetime import datetime

from app import db
from app.models.Log_middleware import LogMiddleware
from flask import Request


class Log_Middleware:
    """
    Contains function for log middleware
    """

    def __init__(self, app):
        self.app = app
        # self.logger=logging.getLogger('request_logger')
        # self.logger.setLevel(logging.INFO)
        # handler=RotatingFileHandler("request.log",maxBytes=10000,backupCount=1)
        # self.logger.addHandler(handler)

    def __call__(self, environment, start_response, **kwargs):
        """
        Returns request details
        """
        request = Request(environment)

        request_data = {
            'request_url': request.url,
            'ip_address': request.remote_addr,
            'created_at': datetime.utcnow()
        }
        log_entry = LogMiddleware(**request_data)
        db.session.add(log_entry)
        db.session.commit()

        return self.app(environment=environment, start_response=start_response, **kwargs)
