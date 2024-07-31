# from app.models import base

"""
To create log middleware
"""
from datetime import datetime

from app import db


class LogMiddleware(db.Model):
    """
    Contains column details for table
    """
    __tablename__ = 'log_middleware'

    id = db.Column(db.Integer, primary_key=True)
    request_url = db.Column(db.String)
    ip_address = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, request_url, ip_address, created_at):
        """
        Initialize the variables
        """
        self.request_url = request_url
        self.ip_address = ip_address
        self.created_at = created_at
