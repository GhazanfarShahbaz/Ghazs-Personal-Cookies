from dotenv import load_dotenv
from os import getenv, environ
from firebase_admin import credentials, firestore, initialize_app, delete_app

# load local environment containing firebase credentials
load_dotenv()

LOADED: bool = False

def load_environment() -> None:
    """
    Loads the environment variables from Firebase.

    This function loads the environment variables from Firebase by initializing an application with the
    provided credentials and retrieving the environment variables from the specified document in the
    specified collection. The environment variables are then set in the server's environment.

    Returns:
        None.

    Raises:
        None.
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
