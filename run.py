from werkzeug.serving import run_simple # werkzeug development server
from app import application
if __name__ == '__main__':
    run_simple('localhost', 5000, application)