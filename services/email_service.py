import email
import imaplib
from datetime import datetime, timedelta
from email.header import decode_header
from typing import Dict, List

from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD, EMAIL_IMAP_SERVER, OVERNIGHT_HOURS


def _decode_str(value) -> str:
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value or ""


def get_overnight_emails() -> List[Dict]:
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        return []

    since_str = (datetime.now() - timedelta(hours=OVERNIGHT_HOURS)).strftime("%d-%b-%Y")
    messages = []

    try:
        with imaplib.IMAP4_SSL(EMAIL_IMAP_SERVER) as mail:
            mail.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            mail.select("INBOX")

            _, nums = mail.search(None, f'(SINCE "{since_str}" UNSEEN)')
            for num in nums[0].split()[-20:]:  # cap at 20
                _, data = mail.fetch(num, "(RFC822)")
                msg = email.message_from_bytes(data[0][1])

                raw_subject, enc = decode_header(msg["Subject"] or "")[0]
                subject = raw_subject.decode(enc or "utf-8", errors="replace") if isinstance(raw_subject, bytes) else raw_subject

                messages.append(
                    {
                        "from": msg.get("From", "Unknown"),
                        "subject": _decode_str(subject),
                        "time": msg.get("Date", ""),
                    }
                )
    except Exception as exc:
        print(f"[email_service] Failed to fetch emails: {exc}")

    return messages
