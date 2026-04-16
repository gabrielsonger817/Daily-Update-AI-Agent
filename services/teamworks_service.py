"""
Teamworks integration.

Teamworks does not publish a fully open REST API; contact their support team
(developer@teamworksathletics.com) to get API credentials and confirm the
correct endpoint paths for your organization.  The implementation below
follows common REST conventions and will need to be adjusted once you have
their official API documentation.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List

import requests

from config import TEAMWORKS_API_KEY, TEAMWORKS_ORG_ID, OVERNIGHT_HOURS

_BASE_URL = "https://api.teamworksathletics.com/v1"


def get_teamworks_messages() -> List[Dict]:
    if not TEAMWORKS_API_KEY or not TEAMWORKS_ORG_ID:
        return []

    since = (datetime.now(timezone.utc) - timedelta(hours=OVERNIGHT_HOURS)).isoformat()
    headers = {
        "Authorization": f"Bearer {TEAMWORKS_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = []
    try:
        resp = requests.get(
            f"{_BASE_URL}/organizations/{TEAMWORKS_ORG_ID}/messages",
            headers=headers,
            params={"since": since, "limit": 20},
            timeout=10,
        )
        resp.raise_for_status()
        for msg in resp.json().get("messages", []):
            messages.append(
                {
                    "from": msg.get("sender_name", "Unknown"),
                    "content": msg.get("body", "")[:200],
                    "time": msg.get("created_at", ""),
                }
            )
    except Exception as exc:
        print(f"[teamworks_service] Failed to fetch messages: {exc}")

    return messages
