from dotenv import load_dotenv
from os import getenv, environ
from firebase_admin import credentials, firestore, initialize_app, delete_app

# load local environment containing firebase credentials
load_dotenv()

LOADED: bool = False

def load_environment() -> None:
    """
    Loads environment into machine from firebase store 
    """
    
    global LOADED

    if LOADED:
        return
    
    LOADED = True
    
    cred = credentials.Certificate(getenv("FIRESTORE_TOKEN"))
    application = initialize_app(cred) 
    
    db = firestore.client()
    environment_vars = db.collection(getenv("FIRESTORE_SERVER")).document(getenv("FIRESTORE_ENVIRONMENT_ID")).get().to_dict()
    
    # delete app so it doesnt conflict with other applications
    delete_app(application)
    
    # place each key into environment
    for key, value in environment_vars.items():
        environ[key] = value
