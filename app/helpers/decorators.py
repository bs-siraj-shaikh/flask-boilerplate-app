"""All custom decorators are defined in this file."""
from functools import wraps
import logging
import time
from typing import Callable

from app import config_data
from app import logger
from app.helpers.constants import HttpStatusCode
from app.helpers.constants import ResponseMessageKeys
from app.helpers.utility import send_json_response
from app.models.student import Student
from app.models.user import User
from flask import g
from flask import request
import jwt


def token_required_student(f: Callable) -> Callable:
    """To check if the request contains a valid student token.
    1. Decodes the token from the request and gets the student details from the database.
    2. Cross-checks the token against the stored auth_token of the student.
    3. If the token is valid, it allows access to the API, else denies access to the request.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        """This method validates the token with the database token."""
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            logging.error('Token is missing!')
            return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                      message_key=ResponseMessageKeys.INVALID_TOKEN.value,
                                      data=None,
                                      error=None)
        try:

            data = jwt.decode(jwt=token, key=config_data.get(
                'SECRET_KEY'), algorithms=['HS256'])
            logging.info(f'Decoded token data: {data}')
            current_student = Student.query.filter_by(id=data['id']).first()

            if current_student:
                logging.info(f'Current student found: {current_student.id}')
                if current_student.auth_token != token:
                    logging.error('Auth token does not match!')
                    return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                              message_key=ResponseMessageKeys.INVALID_TOKEN.value,
                                              data=None,
                                              error=None)
            else:
                logging.error(f"No student found with id {data['id']}")
                return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                          message_key=ResponseMessageKeys.USER_NOT_EXIST.value,
                                          data=None,
                                          error=None)

        except jwt.ExpiredSignatureError:
            logging.error('Token has expired')
            return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                      message_key=ResponseMessageKeys.TOKEN_EXPIRED.value,
                                      data=None,
                                      error=None)
        except jwt.InvalidTokenError:
            logging.error('Token is invalid')
            return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                      message_key=ResponseMessageKeys.INVALID_TOKEN.value,
                                      data=None,
                                      error=None)
        except Exception as e:
            logging.error(f'An error occurred: {str(e)}')
            return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                      message_key=ResponseMessageKeys.INVALID_TOKEN.value,
                                      data=None,
                                      error=None)

        # returns the current logged in student's context to the routes
        request.student_id = current_student.id
        return f(*args, current_student=current_student, **kwargs)

    return decorated


def token_required(f: Callable) -> Callable:  # type: ignore  # noqa: C901
    """To check request contains valid token.
    1. Decodes the token from request and gets the user details from db
    2. If user type is admin then it just cross checks token against auth_token column of user token
    3. If user is owner/crew then it verifies the db to confirm if user belongs to org_id in jwt
    5. If user is a crew in the org_id then we check if they have the permission optionally passed with the url rule: if permission if not found then we return access denied.
    4. If yes then it also cross checks the token with the token saved in the device token dict in user table
    5. If found to match then it allows access to the api else denies access to the request"""
    @wraps(f)
    def decorated(*args, **kwargs):
        """This method validates token with DB token."""
        token = None

        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        # return 401 if token is not passed
        if not token:
            return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                      message_key=ResponseMessageKeys.INVALID_TOKEN.value,
                                      data=None,
                                      error=None)
        try:

            # decoding the payload to fetch the stored details
            data = jwt.decode(jwt=token, key=config_data.get(
                'SECRET_KEY'), algorithms=['HS256'])
            current_user = User.query \
                .filter_by(id=data['id']) \
                .first()

            if current_user:
                if current_user.auth_token != token:
                    return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                              message_key=ResponseMessageKeys.INVALID_TOKEN.value,
                                              data=None,
                                              error=None)

            else:
                return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                          message_key=ResponseMessageKeys.USER_NOT_EXIST.value,
                                          data=None,
                                          error=None)

        except Exception as e:
            logger.info('we got exception {}'.format(e))
            return send_json_response(http_status=HttpStatusCode.UNAUTHORIZED.value, response_status=False,
                                      message_key=ResponseMessageKeys.INVALID_TOKEN.value,
                                      data=None,
                                      error=None)
        # returns the current logged in users contex to the routes
        # We are storing user_id in request params for audit_log table.
        request.user_id = current_user.id
        return f(current_user, *args, **kwargs)  # type: ignore  # noqa: FKA100

    return decorated


def api_time_logger(method: Callable) -> Callable:
    """To return total request time.
    1. takes time at start
    2. performs 'method'
    3. takes time at end: after method returns a response
    4. Calculates the difference and inserts in the api log table to keep track of how long the method took to execute
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        """This method calculate time difference."""
        start = time.time()
        response = method(*args, **kwargs)
        end = time.time()
        g.time_log = round(end - start, 5)  # type: ignore  # noqa: FKA100
        return response
    return wrapper
