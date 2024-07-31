"""
To create app instance
"""

from app import create_app
from app.helpers.middleware import Log_Middleware


application, mail = create_app()


application.wsgi_app = Log_Middleware(application.wsgi_app)

if __name__ == '__main__':
    application.run(debug=True)
