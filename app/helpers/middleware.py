"""
To create log middleware instance to get log data
"""

from datetime import datetime

from app import create_app
from app import db
from app.models.Log_middleware import LogMiddleware
from flask import Request


app, mail = create_app()


class Log_Middleware:

    """
    Middleware for logging requests
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response, **kwargs):
        """
        Log request details and pass the request to the Flask app
        """
        request = Request(environ)
        with app.app_context():

            log_entry = {
                'request_url': request.url,
                'ip_address': request.remote_addr,
                'created_at': datetime.utcnow()
            }
            db.session.add(LogMiddleware(**log_entry))
            db.session.commit()
        # print(f"Request Log: {log_entry}")

        return self.app(environ=environ, start_response=start_response, **kwargs)
