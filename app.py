from werkzeug.middleware.dispatcher import \
    DispatcherMiddleware  # use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.serving import run_simple  # werkzeug development server

from tool_repository.requests import app


def set_up_application():
    application: DispatcherMiddleware = DispatcherMiddleware(app)

    return application


if __name__ == '__main__':
    run_simple('localhost', 5000, set_up_application())
