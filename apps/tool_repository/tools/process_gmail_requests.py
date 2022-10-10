from bs4 import BeautifulSoup

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from typing import Dict

import base64
import json
import tempfile


def create_authorization_file(authorization_dict: Dict) -> tempfile:
    authorization_file: tempfile = tempfile.NamedTemporaryFile()

    authorization_file.write(
        json.dumps(authorization_dict).encode('utf-8')
    )

    authorization_file.flush()
    return authorization_file


def get_credentials(authorization_dict: Dict) -> Credentials:
    authorization_file: tempfile = create_authorization_file(
        authorization_dict)
    creds: Credentials = Credentials.from_authorized_user_file(
        authorization_file.name)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    authorization_file.close()
    return creds


def extract_full_email(msg) -> dict:
    try:
        payload = msg["payload"]
        headers = payload['headers']
        subject, sender = None, None

        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']

        # The Body of the message is in Encrypted format. So, we have to decode it.
        # Get the data and decode it with base 64 decoder.
        parts = payload.get('parts')[0]
        data = parts['body']['data']
        data = data.replace("-", "+").replace("_", "/")
        decoded_data = base64.b64decode(data)

        # Now, the data obtained is in lxml. So, we will parse
        # it with BeautifulSoup library
        soup = BeautifulSoup(decoded_data, "lxml")
        body = soup.body()

        return {
            "Labels": msg["labelIds"],
            "Snippet": msg["snippet"],
            "Subject": str(subject),
            "Sender": str(sender),
            "Message": str(body)
        }
    except:
        return {"Labels": None}


def get_emails(authorization_dict: Dict, label_filters: list, max_results: int, get_snippet: bool) -> dict:
    creds: Credentials = get_credentials(authorization_dict)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # We can also pass maxResults to get any number of emails. Like this:
    results = service.users().messages().list(
        userId='me', labelIds=label_filters, maxResults=max_results).execute()
    messages: list = results.get('messages')

    email_data: Dict = {}
    size: int = 0

    for message in messages:
        msg = service.users().messages().get(
            userId='me', id=message['id']).execute()

        if get_snippet is True:
            subject, sender = None, None
            try:
                payload = msg["payload"]
                headers = payload['headers']

                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']
            except:
                None

            email_data[size] = {
                "Labels": msg["labelIds"],
                "Snippet": msg["snippet"],
                "Subject": str(subject),
                "Sender": str(sender),
            }
        else:
            email_data[size] = extract_full_email(msg)

        size += 1

    return email_data
