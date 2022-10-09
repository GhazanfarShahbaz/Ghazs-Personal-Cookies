import logging.config

from datetime import datetime
from flask import Flask
from flask import request, send_from_directory

app = Flask(
    __name__,
    static_url_path='',
    static_folder='/home/ghaz/personal_website/build',
    template_folder='/home/ghaz/personal_website/build'
)


logging.config.fileConfig('/home/ghaz/flask_gateway/logging.conf')
app.logger = logging.getLogger('MainLogger')

fh = logging.FileHandler('logs/{:%Y-%m-%d}.log'.format(datetime.now()))
formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
fh.setFormatter(formatter)
app.logger.addHandler(fh)


@app.route("/")
def home_route():
    app.logger.info(f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/projects")
def projects_route():
    app.logger.info(f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/skills")
def skills_route():
    app.logger.info(f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/education")
def education_route():
    app.logger.info(f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/resume")
def resume_route():
    app.logger.info(f'Someone accessed the website {request.remote_addr} {request.path}')
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True)
