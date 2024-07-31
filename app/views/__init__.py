"""Contain all the urls of apis"""
from app.views.common_view import AuditView
from app.views.common_view import FileView
from app.views.student_view import StudentView
from app.views.user_view import UserView
from flask import Blueprint
from flask import g
from flask import request
# from app.views.common_view import FileView
# template_dir = os.path.abspath('app/views/users')
v1_blueprints = Blueprint(name='v1', import_name='api1')


@v1_blueprints.before_request
def before_blueprint():
    """This method executed in the beginning of the request."""
    g.time_log = 0
    g.request_path = request.path


@v1_blueprints.after_request
def after_blueprint(response):
    """This method executed in the end of the request."""
    response.headers['Time-Log'] = g.time_log
    # logger.info(f'{response.status_code}: {g.request_path}: {g.time_log}')
    # Uncomment above line while debugging to see API response time in logger file.
    return response


v1_blueprints.add_url_rule(
    '/user/auth', view_func=UserView.login, methods=['POST'])
v1_blueprints.add_url_rule(
    '/user/get', view_func=UserView.search, methods=['GET'])
v1_blueprints.add_url_rule(
    '/common/upload-file', view_func=FileView.as_view('upload'), methods=['POST'])
v1_blueprints.add_url_rule(
    '/log/audit', view_func=AuditView.list, methods=['GET'])
v1_blueprints.add_url_rule(
    '/log/audit-detail', view_func=AuditView.details, methods=['GET'])

v1_blueprints.add_url_rule(
    '/student/login', view_func=StudentView.login_student, methods=['POST'])
v1_blueprints.add_url_rule(
    '/student/get', view_func=StudentView.get_students, methods=['GET'])
v1_blueprints.add_url_rule(
    '/student/get/<int:id>', view_func=StudentView.get_student_by_id, methods=['GET'])
v1_blueprints.add_url_rule(
    '/student/add', view_func=StudentView.add_students, methods=['POST'])
v1_blueprints.add_url_rule(
    '/student/update', view_func=StudentView.update_student_by_token, methods=['PUT'])
v1_blueprints.add_url_rule(
    '/student/delete/<int:id>', view_func=StudentView.delete_student_by_id, methods=['DELETE'])
v1_blueprints.add_url_rule(
    '/student/change_password', view_func=StudentView.change_password, methods=['POST'])
