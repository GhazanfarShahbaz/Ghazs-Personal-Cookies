from wsgiref.simple_server import make_server

# from apps.falcon_apps.file_transporter
from apps.falcon_apps.file_transporter.resources.register.register_machine_resource import RegisterMachineResource

# from apps.falcon_apps.file_transporter.resources.upload.folder_resource import FolderZipResource
# from apps.falcon_apps.file_transporter.resources.upload.file_resource import FileResource

from apps.falcon_apps.file_transporter.utils.middleware import Middleware

import falcon


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = (
            '\nTwo things awe me most, the starry sky '
            'above me and the moral law within me.\n'
            '\n'
            '    ~ Immanuel Kant\n\n'
        )


# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', things)
app.add_route('/register', RegisterMachineResource)


# app = falcon.API(middleware=[Middleware()])
# app.add_route('/upload/folder-zip', FolderZipResource())
# app.add_route('/upload/file', FileResource())