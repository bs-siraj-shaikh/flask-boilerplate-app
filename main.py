# Importing libraries
"""
This is the main file for the application.
It creates the flask app and runs it.
"""
from app import create_app
application = create_app()


if __name__ == '__main__':
    application.run(host='0.0.0.0')  # type: ignore  # noqa: attribute-error
