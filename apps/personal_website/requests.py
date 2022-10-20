import logging.config

from flask import Flask
from flask import request, send_from_directory

app = Flask(
    __name__,
    static_url_path='',
    static_folder='./personal_website/build',
    template_folder='./personal_website/build'
)

logging.config.fileConfig('/home/ghaz/flask_gateway/logging.conf')
app.logger = logging.getLogger('MainLogger')


handler = logging.handlers.TimedRotatingFileHandler(
'logs/app.log', when="midnight")

handler.prefix = "%Y%m%d"

formatter = logging.Formatter('%(asctime)s | %(pathname)s | %(levelname)-8s | %(filename)s-%(funcName)s-%(lineno)04d | %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)


@app.route("/")
def home_route():
    app.logger.info(
        f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/projects")
def projects_route():
    app.logger.info(
        f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/skills")
def skills_route():
    app.logger.info(
        f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/education")
def education_route():
    app.logger.info(
        f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/resume")
def resume_route():
    app.logger.info(
        f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True)
