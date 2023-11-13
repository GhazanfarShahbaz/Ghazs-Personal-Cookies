"""
file_name = authentication_blueprint.py
Created On: 2023/11/12
Lasted Updated: 2023/11/12
Description: _FILL OUT HERE_
Edit Log:
2023/11/12
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from datetime import datetime, timedelta
from os import environ
from typing import Final, Tuple, TypeAlias, TypedDict
...

# THIRD PARTY LIBRARY IMPORTS
from firebase_admin import credentials, firestore, initialize_app
from flask import Blueprint, request
from hashlib import sha256
from uuid import uuid4
...

# LOCAL LIBRARY IMPORTS
...

authentication_blueprint: Blueprint = Blueprint("authenticate", __name__)

CREDENTIALS = credentials.Certificate(environ["FIRESTORE_TOKEN"])
initialize_app(CREDENTIALS, name="TEST")

Token: TypeAlias = str

class TokenMetadata(TypedDict):
    token_owner: str        # Token owner name, firebase username
    created_on: datetime    # Date token was created
    expires_on: datetime    # Date token expires


class TokenHandler:
    token_duration: Final[int] = 3600
    
    def __init__(self) -> None:
        self.tokens: Dict[Token, TokenMetadata] = {}

    # PUBLIC METHODS START HERE
    
    def create_and_register_token(self,username: str, password: str) -> Token: 
        if not self._validate_user(username, password):
            raise ValueError("Invalid username or password")
        
        return self._generate_and_register_token(username)

    def validate_token(self, username: str, token: Token) -> dict:
        if not token in self.tokens:
            return  {
                "ErrorCode": 1,
                "ErrorString": "Invalid Token"
            }
            
        token_metadata: TokenMetadata = self.tokens[token]

        if token_metadata.username != username:
            return  {
                "ErrorCode": 1,
                "ErrorString": "Invalid Token"
            }
            
        current_time: datetime = datetime.now()
        
        if current_time > token_metadata.expires_on:
            del self.tokens[token]
            
            return  {
                "ErrorCode": 2,
                "ErrorString": "Token Expired"
            }
        
        return {
            "ErrorCode": 0,
            "ErrorString": "Successfully Validated"
        }
    
    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE
    
    def _generate_and_register_token(self, username: str) -> Token:
        token: Token = None
        valid_token: bool = False

        # Generate till we obtain a unique token
        while not valid_token:
            uuid: int = uuid4()
            token: Token = sha256(str(uuid).encode("UTF-8")).hexdigest()
            
            if not token in self.tokens.keys():
                valid_token = True
            
        created_on: datetime = datetime.now()
        expires_on: datetime = created_on + timedelta(seconds = self.token_duration)
        
        metadata: TokenMetadata = TokenMetadata(
            {
                "username": username,
                "created_on": created_on,
                "expires_on": expires_on
            }
        )
        
        # Register token
        self.tokens[token] = metadata
        return token
    
    def _validate_user(self, username: str, password: str) -> bool:
        firestore_client = firestore.client()
        users_ref = firestore_client.collection(environ["FIRESTORE_SERVER"])

        token = users_ref.document(environ["FIRESTORE_DOC_ID"]).get().to_dict()        
        if (username and username == token["username"]) and (password and password == token["password"]):
            return True

        return False
        
    
    # PRIVATE METHODS END HERE
    
    

token_handler: TokenHandler = TokenHandler()

@authentication_blueprint.route("/grantAuthenticationToken", methods=["POST"])
def grant_authentication_token():
    request_form = request.json
    
    token: Token = token_handler.create_and_register_token(request_form.get("username"), request_form.get("password"))
    
    return {
        "token": token
    }
    
@authentication_blueprint.route("/validateAuthenticationToken", methods=["POST"])
def validate_authentication_token():
    request_form = request.json
    
    return token_handler.validate_token(request_form.get("username"), request_form.get("token"))