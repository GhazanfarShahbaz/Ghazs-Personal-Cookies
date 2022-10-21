import logging.config

from flask import Flask, abort
from flask import request, send_from_directory

# Create flask app. Static and template folder point to personal website react build files
app = Flask(
    __name__,
    static_url_path='',
    static_folder='/home/ghaz/PersonalWebsite/build',
    template_folder='/home/ghaz/PersonalWebsite/build'
)

# Set logger config
logging.config.fileConfig('/home/ghaz/flask_gateway/logging.conf')
app.logger = logging.getLogger('MainLogger')

# Handler for log file. So log files are rotated everyday
handler = logging.handlers.TimedRotatingFileHandler(
'logs/app.log', when="midnight")
handler.prefix = "%Y%m%d"

# Formatter for log file. Log files will be formatted in the format specified below
formatter = logging.Formatter('%(asctime)s | %(pathname)s | %(levelname)-8s | %(filename)s-%(funcName)s-%(lineno)04d | %(message)s')
handler.setFormatter(formatter)

# Add handler to the app logger
app.logger.addHandler(handler)

@app.before_request   
def log_endpoint():
    """
        Log endpoint with ip address and path accessed
    """
    app.logger.info(f'Someone accessed the website {request.remote_addr} {request.path}')


@app.route("/")
def home_route():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path>')
def render_path(path: str):
    # accept paths which we have files for
    if path in {"projects", "skills", "education", "resume"}:
        return send_from_directory(app.static_folder, 'index.html')
    elif path in {"robots.txt", "sitemap.xml"}:
        return send_from_directory(app.root_path + "/static/", path)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
