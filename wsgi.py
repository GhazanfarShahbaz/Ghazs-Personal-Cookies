from apps.personal_website.requests import app as personal_website_app
from apps.tool_repository.endpoints import app as tool_app
from apps.projects.the_mouseion.app import app as mouseion_app

# use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.middleware.dispatcher import DispatcherMiddleware


def set_up_application() -> DispatcherMiddleware:
    """
    Creates a dispatcher middleware that combines multiple Flask applications.

    This function creates a Flask dispatcher middleware that combines multiple Flask applications,
    including `personal_website_app`, `tool_app`, and `mouseion_app`, and returns the resulting middleware.
    The resulting middleware can be run like a Flask application.

    Returns:
        A DispatcherMiddleware object.

    Raises:
        None.
    """

    application: DispatcherMiddleware = DispatcherMiddleware(
        personal_website_app, {"/tools": tool_app, "/the_mouseion": mouseion_app}
    )

    return application


app = set_up_application()
