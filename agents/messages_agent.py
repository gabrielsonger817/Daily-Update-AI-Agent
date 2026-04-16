from typing import Dict, List

from services.email_service import get_overnight_emails
from services.sms_service import get_received_sms
from services.teamworks_service import get_teamworks_messages


def get_overnight_messages() -> Dict[str, List]:
    return {
        "emails": get_overnight_emails(),
        "sms": get_received_sms(),
        "teamworks": get_teamworks_messages(),
    }
