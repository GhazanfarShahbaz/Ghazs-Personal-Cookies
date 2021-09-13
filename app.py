from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from tool_repository.requests import app

application = DispatcherMiddleware(app)