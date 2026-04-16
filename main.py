"""
Entry point for the Daily Update AI Agent.

Usage:
  python main.py          — start the scheduler (runs at the configured time every day)
  python main.py --now    — run immediately (useful for testing)
"""

import logging
import sys
from datetime import datetime

import pytz

from config import TIMEZONE
from agents.news_agent import get_top_news
from agents.weather_agent import get_weather
from agents.stocks_agent import get_stock_data
from agents.messages_agent import get_overnight_messages
from agents.briefing_agent import compile_briefing
from services.sms_service import send_sms

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("daily_update.log"),
    ],
)
log = logging.getLogger(__name__)


def run_daily_update() -> str:
    tz = pytz.timezone(TIMEZONE)
    log.info("Daily update started — %s", datetime.now(tz).strftime("%Y-%m-%d %H:%M %Z"))

    log.info("Fetching weather…")
    weather = get_weather()

    log.info("Fetching news…")
    news = get_top_news()

    log.info("Fetching stock data…")
    stocks = get_stock_data()

    log.info("Fetching overnight messages…")
    messages = get_overnight_messages()

    log.info("Compiling briefing with Claude…")
    briefing = compile_briefing(weather, news, stocks, messages)

    log.info("Sending SMS…")
    send_sms(briefing)

    log.info("Daily update sent successfully.")
    return briefing


if __name__ == "__main__":
    if "--now" in sys.argv:
        result = run_daily_update()
        print("\n" + "─" * 60)
        print(result)
        print("─" * 60)
    else:
        from scheduler import start_scheduler
        start_scheduler()
