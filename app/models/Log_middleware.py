# from app.models import base
from datetime import datetime

from app import db


class LogMiddleware(db.Model):
    """
    Contains column details for table
    """
    id = db.Column(db.Integer, primary_key=True)
    request_url = db.Column(db.String)
    ip_address = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
