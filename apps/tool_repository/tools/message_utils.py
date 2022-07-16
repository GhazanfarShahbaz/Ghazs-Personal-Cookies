import os 

from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
ph="+19144154844"


def get_client():
    return Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))

def send_message(message: str):
    client = get_client()
    
    client.api.account.messages.create(
        to="+13475936743",
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        body="Hello there!"
    )
    
send_message("TEST")