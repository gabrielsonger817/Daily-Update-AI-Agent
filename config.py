import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Anthropic
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

# Twilio
TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER: str = os.getenv("TWILIO_FROM_NUMBER", "")
MY_PHONE_NUMBER: str = os.getenv("MY_PHONE_NUMBER", "")

# News API
NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")

# OpenWeatherMap
OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
MY_CITY: str = os.getenv("MY_CITY", "New York")
MY_COUNTRY_CODE: str = os.getenv("MY_COUNTRY_CODE", "US")

# Stock watchlist — user-defined tickers
_raw_watchlist: str = os.getenv("STOCK_WATCHLIST", "SPY,QQQ,AAPL,GOOGL,MSFT")
STOCK_WATCHLIST: List[str] = [s.strip().upper() for s in _raw_watchlist.split(",") if s.strip()]

# Gmail / IMAP
EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS", "")
EMAIL_APP_PASSWORD: str = os.getenv("EMAIL_APP_PASSWORD", "")
EMAIL_IMAP_SERVER: str = os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com")

# Teamworks
TEAMWORKS_API_KEY: str = os.getenv("TEAMWORKS_API_KEY", "")
TEAMWORKS_ORG_ID: str = os.getenv("TEAMWORKS_ORG_ID", "")

# Schedule
UPDATE_HOUR: int = int(os.getenv("UPDATE_HOUR", "8"))
UPDATE_MINUTE: int = int(os.getenv("UPDATE_MINUTE", "45"))
TIMEZONE: str = os.getenv("TIMEZONE", "America/New_York")

# How many hours back to look for overnight messages
OVERNIGHT_HOURS: int = int(os.getenv("OVERNIGHT_HOURS", "12"))
