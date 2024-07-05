"""Contains user related API definitions."""
from datetime import datetime
from datetime import timedelta
import re

from app import config_data
from app import db
from app.helpers.constants import HttpStatusCode
from app.helpers.constants import ResponseMessageKeys
from app.helpers.decorators import api_time_logger
from app.helpers.decorators import token_required_student
from app.helpers.utility import get_pagination_meta
from app.helpers.utility import send_json_response
from app.models.student import Student
from flask import request
from flask.views import View
import jwt
from providers.mail import send_mail
# from flask_jwt_extended import create_access_token


class StudentView(View):
    """
    Contains all student related functions
    """

    def create_auth_response(self, student: Student):
        """Returns student details and access token
        """

        token = jwt.encode({
            'id': student.id,
            'exp': datetime.utcnow() + timedelta(days=60)
        }, key=config_data.get('SECRET_KEY'))

        student_details = {
            'id': student.id,
            'name': student.name,
            'clas': student.clas,
            'division': student.division,
            'email': student.email,
            'password': student.password
        }
        student.auth_token = token
        db.session.commit()

        response = {'token': token, 'student': student_details,
                    'message': 'Successfully login'}
        return send_json_response(http_status=HttpStatusCode.OK.value, response_status=True,
                                  message_key=ResponseMessageKeys.SUCCESS.value,
                                  data=response)
        # return response

    @staticmethod
    @api_time_logger
    def get_students():
        '''
        Returns result and pagination metadata
        '''
        name = request.args.get('name')
        page = request.args.get('page')
        size = request.args.get('size')
        sort = request.args.get('sort')

        students = Student.get_student(
            name=name, page=page, size=size, sort=sort)
        total_count = Student.count(name=name)

        student_data = Student.serialize_student(students)
        pagination_meta = get_pagination_meta(
            current_page=1 if page is None else int(page),
            page_size=int(size) if size else len(students),
            total_items=int(total_count)
        )
        data = {
            'result': student_data,
            'pagination_metadata': pagination_meta
        }
        return send_json_response(http_status=HttpStatusCode.OK.value, response_status=True,
                                  message_key=ResponseMessageKeys.SUCCESS.value, data=data,
                                  error=None)

    @staticmethod
    @api_time_logger
    def add_students():
        """
        To add student and check required fields
        """

        try:
            data = request.json
            required_fields = ['name', 'clas', 'division', 'email', 'password']

            for field in required_fields:
                if field not in data or not data[field]:
                    message = f'Missing or empty field :{field.upper()}'
                    return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value, response_status=False,
                                              message_key=message,
                                              data=None)

            password = data['password']
            if not re.match(pattern=r'^(?=.*[a-zA-Z])(?=.*[0-9])[A-Za-z0-9]{8,}$', string=password):
                message = 'Password must be at least 8 alphanumeric characters'
                return send_json_response(
                    http_status=HttpStatusCode.BAD_REQUEST.value,
                    response_status=False,
                    message_key=message,
                    data=None
                )

            existing_student = Student.query.filter_by(
                email=data['email']).first()
            if existing_student:
                return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value,
                                          response_status=False,
                                          message_key=ResponseMessageKeys.EMAIL_ALREADY_EXISTS.value, data=None)

            student = Student(
                name=data['name'],
                clas=data['clas'],
                division=data['division'],
                email=data['email'],
                password=data['password']
            )
            db.session.add(student)
            db.session.commit()

            student_data = student.to_dict()

            # # Prepare email content
            email_to = data['email']
            subject = 'Welcome to school >>>>>'
            template = 'emails/welcome.html'
            # email_type='welcome'
            email_data = {
                'name': data['name'],
                'clas': data['clas'],
                'division': data['division'],
                'email': data['email'],
                'password': data['password']
            }

            send_mail(email_to=email_to, subject=subject,
                      template=template, data=email_data)
            # print("Newly added student data:", student_data)
            return send_json_response(http_status=HttpStatusCode.OK.value,
                                      response_status=True,
                                      message_key=ResponseMessageKeys.STUDENT_ADDED.value,
                                      data=student_data)
        except Exception as e:
            error_message = str(e)
            return send_json_response(http_status=HttpStatusCode.INTERNAL_SERVER_ERROR.value,
                                      response_status=False,
                                      message_key=ResponseMessageKeys.FAILED.value,
                                      error=error_message)

    # Get student by id
    @staticmethod
    @api_time_logger
    def get_student_by_id(id):
        """
        return student by id
        """

        StudentV1_data = Student.get_student_by_id(id)
        return StudentV1_data
        # return Student_data

    @staticmethod
    @api_time_logger
    @token_required_student
    def update_student_by_token(current_student):
        """
        Returns updated student

        """

        data = request.json
        student = Student.query.filter_by(id=current_student.id).first()
        student = Student.to_dict(student)
        if not student:

            return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value, response_status=True,
                                      message_key=ResponseMessageKeys.USER_NOT_EXIST.value, data=None)
            # return {'message': 'Student not found'}, 404

        if current_student.id != student['id']:
            return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value, response_status=True,
                                      message_key=ResponseMessageKeys.STUDENT_UPDATE_OTHER_DETAILS.value, data=None)
            # return {'message': 'You can only update your own information'}, 403

        # Update the student information
        student['name'] = data.get(key='name', default=student['name'])
        student['clas'] = data.get(key='clas', default=student['clas'])
        student['division'] = data.get(
            key='division', default=student['division'])
        student['email'] = data.get(key='email', default=student['email'])
        if 'password' in data:
            student['password'] = data.get(
                ['password'], default=student['password'])

        db.session.commit()
        return send_json_response(http_status=HttpStatusCode.OK.value, response_status=True,
                                  message_key=ResponseMessageKeys.SUCCESS.value, data=student)

    @staticmethod
    @api_time_logger
    @token_required_student
    def change_password(current_student):
        """
        To change password for student
        """
        # student=Student.query.filter_by(email=email).first()
        data = request.get_json()
        # email=data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password or not new_password:
            return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value,
                                      response_status=False,
                                      message_key=ResponseMessageKeys.EMAIL_PASS_REQUIRED.value,
                                      data=None)
        # import pdb; pdb.set_trace()
        if current_student.password != old_password:
            return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value,
                                      response_status=False,
                                      message_key=ResponseMessageKeys.INVALID_REQUEST.value,
                                      data=None)

        current_student.password = new_password

        db.session.commit()

        # To get student data
        student_data = Student.query.filter_by(
            email=current_student.email).first()
        student_data = Student.serialize_student(student_data)
        # data={'data':student_data}
        return send_json_response(http_status=HttpStatusCode.OK.value,
                                  response_status=True,
                                  message_key=ResponseMessageKeys.SUCCESS.value,
                                  data=student_data)

    @staticmethod
    @api_time_logger
    def delete_student_by_id(id):
        """
        Delete student by id
        """

        student = Student.query.filter_by(id=id).first()
        if not student:
            return send_json_response(
                http_status=HttpStatusCode.BAD_REQUEST.value,
                response_status=False,
                message_key=ResponseMessageKeys.STUDENT_NOT_EXIST.value,
                data=None
            )
        else:
            db.session.delete(student)
            db.session.commit()

            remaining_students = Student.query.all()
            serialized_students = [student.to_dict()
                                   for student in remaining_students]

            return send_json_response(
                http_status=HttpStatusCode.OK.value,
                response_status=True,
                message_key=ResponseMessageKeys.SUCCESS.value,
                data=serialized_students
            )

    @staticmethod
    @api_time_logger
    def login_student():
        """
        Returns auth response
        """

        data = request.json
        email = data['email']
        password = data['password']

        if not email or not password:
            return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value, response_status=False,
                                      message_key=ResponseMessageKeys.STUDENT_DETAILS_MISSING.value, data=None)
            # return {'message':'Missing email or password'}
        student = Student.query.filter_by(email=email).first()

        if student and student.password == password:
            return StudentView().create_auth_response(student=student)
        else:
            return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value, response_status=True,
                                      message_key=ResponseMessageKeys.INVALID_EMAIL_PASSWORD.value, data=None)
            # return {'message':"Invalid email or password"}
