"""
file_name = message_utils.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to work send messages using the twilio api.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""


from os import environ
from twilio.rest import Client


def get_client():
    """
    Creates and returns a twilio client
    Returns:
        Client: A twilio client instance
    """
    return Client(environ["TWILIO_SID"], environ["TWILIO_TOKEN"])


def send_message(message: str):
    """
    Sends a message to a specified phone number using the twilo api.

    Args:
        message: A string containing the message to send

    Returns:
        None
    """
    client = get_client()

    client.api.account.messages.create(
        to="XX", from_=environ["TWILIO_PHONE_NUMBER"], body=message
    )
