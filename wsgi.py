from generate_env import load_environment

load_environment()

from werkzeug.middleware.dispatcher import DispatcherMiddleware  # use to combine each Flask app into a larger one that is dispatched based on prefix

from apps.personal_website.requests import app as personal_website_app
from apps.tool_repository.endpoints import app as tool_app

def set_up_application():
    application: DispatcherMiddleware = DispatcherMiddleware(personal_website_app, {"/tools": tool_app})

    return application

app = set_up_application()

