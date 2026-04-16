from datetime import datetime, timedelta, timezone
from typing import Dict, List

from twilio.rest import Client

from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    MY_PHONE_NUMBER,
    OVERNIGHT_HOURS,
)

_SMS_CHUNK_SIZE = 1500  # stay safely under Twilio's segment limit


def send_sms(message: str) -> None:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    chunks = [message[i : i + _SMS_CHUNK_SIZE] for i in range(0, len(message), _SMS_CHUNK_SIZE)]
    for chunk in chunks:
        client.messages.create(body=chunk, from_=TWILIO_FROM_NUMBER, to=MY_PHONE_NUMBER)


def get_received_sms() -> List[Dict]:
    """Return SMS messages sent TO your Twilio number overnight."""
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
        return []

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    since = datetime.now(timezone.utc) - timedelta(hours=OVERNIGHT_HOURS)

    messages = []
    try:
        for msg in client.messages.list(to=TWILIO_FROM_NUMBER, date_sent_after=since, limit=20):
            messages.append(
                {
                    "from": msg.from_,
                    "body": msg.body[:200],
                    "time": str(msg.date_sent),
                }
            )
    except Exception as exc:
        print(f"[sms_service] Failed to fetch received SMS: {exc}")

    return messages
