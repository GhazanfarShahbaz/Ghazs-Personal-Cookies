import logging
from flask import Flask 
from flask import request, jsonify

app = Flask(__name__)
logging.basicConfig(filename='logs/personal_website_requests.log', level=logging.DEBUG)

@app.route("/")
def home_route():
    app.logger.info(f'Someone accessed the website {request.remote_addr}')
    return "This site is under maintenance"

if __name__ == "__main__":
    app.run(debug=True)