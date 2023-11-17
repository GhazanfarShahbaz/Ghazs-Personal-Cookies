"""
file_name = wsgi.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/08/2023
Description: A file used to combine flask applications and serve them as one wsgi application.
Edit Log: 
07/08/2023 
    - Refactored personal_website new flask file name
08/05/2023
    - Added questions application
"""

# use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# FLASK APPS START HERE
from apps.personal_website.app import app as personal_website_app
from apps.tool_repository.app import app as tool_app
from apps.knowledge_graph.app import app as knowledge_graph_app
from apps.projects.the_mouseion.app import app as mouseion_app
from apps.coding_questions.app import app as coding_questions_app
from apps.obsidian_connector.app import app as obsidian_connector_app
# FLASK APPS END HERE

# FALCON APPS START HERE
from apps.falcon_apps.file_transporter.app import app as file_transporter_app
# FALCON APPS END HERE 



def set_up_application() -> DispatcherMiddleware:
    """
    Creates a dispatcher middleware that combines multiple Flask applications.

    This function creates a Flask dispatcher middleware that combines multiple Flask applications,
    including `personal_website_app`, `tool_app`, and `mouseion_app`, and returns the resulting 
    middleware.
    The resulting middleware can be run like a Flask application.

    Returns:
        A DispatcherMiddleware object.

    Raises:
        None.
    """

    application: DispatcherMiddleware = DispatcherMiddleware(
        personal_website_app,
        {
            "/tools": tool_app,
            "/the_mouseion": mouseion_app,
            "/knowledge_graph": knowledge_graph_app,
            "/coding_questions": coding_questions_app,
            "/obsidian_connector": obsidian_connector_app,
            # FALCON APPS START HERE 
            "/file_transporter": file_transporter_app
            # FALCON APPS END HERE
        },
    )

    return application


app = set_up_application()
