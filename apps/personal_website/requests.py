import logging
from flask import Flask 
from flask import request, redirect, send_from_directory

app = Flask(__name__, static_url_path='', static_folder='/home/ghaz/personal_website/build', template_folder='/home/ghaz/personal_website/build')
logging.basicConfig(filename='logs/personal_website_requests.log', level=logging.DEBUG)

@app.route("/")
def home_route():
    app.logger.info(f'Someone accessed the website {request.remote_addr}')
    # return redirect("http://www.ghazanfarshahbaz.dev", code=302)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)