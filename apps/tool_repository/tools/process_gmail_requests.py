from bs4 import BeautifulSoup

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from typing import Dict

import base64
import json
import tempfile


def create_authorization_file(authorization_dict: Dict) -> tempfile:
    """
    Creates a temporary file containing authorization information.

    This function takes a dictionary `authorization_dict` representing authorization information and writes it to a new temporary
    file. The function returns a handle to the temporary file.

    Args:
        authorization_dict: A dictionary containing authorization information.

    Returns:
        A handle to a temporary file containing the authorization information.
    """

    authorization_file: tempfile = tempfile.NamedTemporaryFile()

    authorization_file.write(json.dumps(authorization_dict).encode("utf-8"))

    authorization_file.flush()
    return authorization_file


def get_credentials(authorization_dict: Dict) -> Credentials:
    """
    Retrieves user credentials from a temporary file.

    This function takes a dictionary `authorization_dict` containing authorization information and creates a temporary file.
    The function then reads the credentials from the temporary file and returns them as a `Credentials` object.

    Args:
        authorization_dict: A dictionary containing authorization information.

    Returns:
        A `Credentials` object containing the user's credentials.
    """

    authorization_file: tempfile = create_authorization_file(authorization_dict)
    creds: Credentials = Credentials.from_authorized_user_file(authorization_file.name)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    authorization_file.close()
    return creds


def extract_full_email(msg) -> dict:
    """
    Extracts specific fields from an email message.

    This function takes an email message `msg` and extracts specific fields from it. The fields that are extracted include
    the email labels, snippet, subject, sender, and message text. The function returns a dictionary containing the extracted
    fields.

    Args:
        msg: An email message.

    Returns:
        A dictionary containing the extracted email fields.
    """

    try:
        payload = msg["payload"]
        headers = payload["headers"]
        subject, sender = None, None

        for d in headers:
            if d["name"] == "Subject":
                subject = d["value"]
            if d["name"] == "From":
                sender = d["value"]

        # The Body of the message is in Encrypted format. So, we have to decode it.
        # Get the data and decode it with base 64 decoder.
        parts = payload.get("parts")[0]
        data = parts["body"]["data"]
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
            "Message": str(body),
        }
    except:
        return {"Labels": None}


def get_emails(
    authorization_dict: Dict, label_filters: list, max_results: int, get_snippet: bool
) -> dict:
    """
    Retrieves a list of email messages from Gmail.

    This function takes a dictionary `authorization_dict` containing authorization information, a list of label filters `label_filters`,
    an integer `max_results` representing the maximum number of email messages to retrieve, and a boolean `get_snippet` indicating
    whether to retrieve only the email header or also the full email body. The function then connects to the Gmail API using the
    provided authorization information, retrieves a list of email messages based on the provided label filters and maximum number
    of results, and returns a dictionary containing the email labels, subject, sender, snippet and message text for each email.

    Args:
        authorization_dict: A dictionary containing the authorization information for the Gmail API.
        label_filters: A list of strings containing label filters to apply when retrieving email messages.
        max_results: An integer representing the maximum number of email messages to retrieve.
        get_snippet: A boolean indicating whether to retrieve only the email header or also the full email body.

    Returns:
        A dictionary containing the email labels, subject, sender, snippet and message text for each email.
    """

    creds: Credentials = get_credentials(authorization_dict)

    # Connect to the Gmail API
    service = build("gmail", "v1", credentials=creds)

    # We can also pass maxResults to get any number of emails. Like this:
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=label_filters, maxResults=max_results)
        .execute()
    )
    messages: list = results.get("messages")

    email_data: Dict = {}
    size: int = 0

    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()

        if get_snippet is True:
            subject, sender = None, None
            try:
                payload = msg["payload"]
                headers = payload["headers"]

                for d in headers:
                    if d["name"] == "Subject":
                        subject = d["value"]
                    if d["name"] == "From":
                        sender = d["value"]
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
