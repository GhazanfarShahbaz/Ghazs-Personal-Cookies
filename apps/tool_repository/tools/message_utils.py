from os import environ
from twilio.rest import Client

ph = "XX"


def get_client():
    return Client(environ["TWILIO_SID"], environ["TWILIO_TOKEN"])


def send_message(message: str):
    client = get_client()

    client.api.account.messages.create(
        to="XX", from_=environ["TWILIO_PHONE_NUMBER"], body=message
    )
