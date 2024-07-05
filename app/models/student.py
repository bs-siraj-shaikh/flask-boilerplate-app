"""Contains student table definitions."""
from __future__ import annotations

from app import db
from app.helpers.constants import HttpStatusCode
from app.helpers.constants import ResponseMessageKeys
from app.helpers.utility import send_json_response
from app.models.base import Base
from flask_restful import fields
from flask_restful import marshal_with

studentFields = {
    'id': fields.Integer,
    'name': fields.String,
    'clas': fields.Integer,
    'email': fields.String,
    'password': fields.String,
    'deleted_at': fields.DateTime,
    'division': fields.String
}


class Student(Base):

    '''
    Contains function related to student model
    '''
    # __tablename__='Student Management System'
    __tablename__ = 'student'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    clas = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=True)
    auth_token = db.Column(db.String, nullable=True)
    division = db.Column(db.String, nullable=False)
    deleted_at = db.Column(db.DateTime)

    @staticmethod
    @marshal_with(studentFields)
    def get_student(name=None, page=None, size=None, sort=None):
        '''
        Returns result and pagination metadata
        '''

        query = Student.query
        if name:
            query = query.filter(Student.name.ilike(f'%{name}%'))

        if sort:
            query = query.order_by(sort)

        if page and size:
            pagination = query.paginate(
                page=int(page), per_page=int(size), error_out=False)
            return pagination.items

        else:
            return query.all()
        # return students

    @staticmethod
    def count(name=None):
        """ Return count based on name """

        query = Student.query
        if name:
            query = query.filter(Student.name.ilike(f'%{name}%'))
        return query.count()

    @staticmethod
    @marshal_with(studentFields)
    def add_student():
        """
        to add student
        """
        try:
            response = Student.add_student()

            return send_json_response(http_status=HttpStatusCode.OK.value, response_status=True,
                                      message_key=ResponseMessageKeys.STUDENT_ADDED.value, data=dict(response))
        except Exception as e:
            return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value, response_status=False, message_key=ResponseMessageKeys.EMAIL_ALREADY_EXISTS.value, data=None, error=str(e))

    def to_dict(self):
        """
        Returns student in dictionary format
        """
        return {
            'id': self.id,
            'name': self.name,
            'clas': self.clas,
            'division': self.division,
            'email': self.email,
            'password': self.password,
            'deleted_at': self.deleted_at
        }

    @staticmethod
    @marshal_with(studentFields)
    def serialize_student(student_list):
        """
        Returns student list
        """

        return student_list

    @staticmethod
    @marshal_with(studentFields)
    def get_student_by_id(id):
        """
        Returns student by id
        """

        student = Student.query.filter_by(id=id).first()
        return student
