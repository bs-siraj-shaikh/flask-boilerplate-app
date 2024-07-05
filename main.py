# Importing libraries
"""
This is the main file for the application.
It creates the flask app and runs it.
"""
from app import create_app
from app.helpers.middleware import Log_Middleware
application, mail = create_app()

application.wsgi_app = Log_Middleware(application.wsgi_app)

if __name__ == '__main__':
    application.run(debug=True)  # type: ignore  # noqa: attribute-error
