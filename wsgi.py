from apps.personal_website.requests import app as personal_website_app
from apps.tool_repository.endpoints import app as tool_app
from apps.projects.the_mouseion.app import app as mouseion_app

# use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.middleware.dispatcher import DispatcherMiddleware

def set_up_application() -> DispatcherMiddleware:
    """
    Creates a dispatcher middleware that combines multiple flask applications

    Returns:
        DispatcherMiddleware: A middleware that can be run like a flask app
    """
    
    application: DispatcherMiddleware = DispatcherMiddleware(
        personal_website_app, 
            {
            "/tools": tool_app,
            "/the_mouseion": mouseion_app,
            }
        )

    return application


app = set_up_application()
