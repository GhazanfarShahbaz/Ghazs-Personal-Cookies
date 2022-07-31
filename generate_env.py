from dotenv import load_dotenv
from os import getenv, environ
from firebase_admin import credentials, firestore, initialize_app, delete_app

load_dotenv()

def load_environment() -> None:
    cred = credentials.Certificate(getenv("FIRESTORE_TOKEN"))
    application = initialize_app(cred) 
    
    db = firestore.client()
    environment_vars = db.collection(getenv("FIRESTORE_SERVER")).document(getenv("FIRESTORE_ENVIRONMENT_ID")).get().to_dict()
    
    delete_app(application)
    
    for key, value in environment_vars.items():
        environ[key] = value
