from werkzeug.middleware.dispatcher import \
    DispatcherMiddleware  # use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.serving import run_simple  # werkzeug development server

from personal_website.requests import app as personal_website_app
from tool_repository.requests import app as tool_app


def set_up_application():
    application: DispatcherMiddleware = DispatcherMiddleware(personal_website_app, {"/tools": tool_app})

    return application



app = DispatcherMiddleware(personal_website_app, {"/tools": tool_app})
# run_simple('localhost', 5000, set_up_application())
