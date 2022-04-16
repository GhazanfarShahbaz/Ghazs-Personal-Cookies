from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from json.tool import main

from typing import Dict

import json
import os
import tempfile


def create_authorization_file(authorization_dict: Dict) -> tempfile:
    authorization_file: tempfile = tempfile.NamedTemporaryFile()
    
    authorization_file.write(
        json.dumps(authorization_file).encode('utf-8')
    )
    
    authorization_file.flush()
    return authorization_file


def get_credentials(authorization_dict: Dict) -> Credentials:
    authorization_file: tempfile = authorization_dict(authorization_dict)
    creds: Credentials = Credentials.from_authorized_user_file(authorization_file)
    authorization_file.close()
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            
    return authorization_file
    
    
def get_emails(authorization_dict: Dict, label_filters: list, max_results: int) -> dict:
    creds: Credentils = get_credentials(authorization_dict)
    
    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
  
    # request a list of all the messages
    result = service.users().messages().list(userId='me').execute()
    
    # We can also pass maxResults to get any number of emails. Like this:
    results = service.users().messages().list(userId='me',labelIds=label_filters, maxResults=max_results).execute()
    messages: list = results.get('messages', [])
    
    email_data: Dict = {}
    size: int = 0
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        
        email_data[size] = {
            "Labels": msg["labelIds"],
            "Snippet": msg["snippet"]
        }
        
        size += 1
        
    return email_data