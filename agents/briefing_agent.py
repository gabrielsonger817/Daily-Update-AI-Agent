"""
Uses Claude to compile all collected data into a concise morning SMS briefing.
Prompt caching is applied to the static system prompt to reduce token costs.
"""

from datetime import datetime
from typing import Dict, List

import anthropic
import pytz

from config import ANTHROPIC_API_KEY, TIMEZONE

_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

_SYSTEM_PROMPT = (
    "You are a personal morning briefing assistant. "
    "Your job is to compile data into a clear, concise SMS update. "
    "Use emoji section headers to aid quick scanning. "
    "Be direct — no filler phrases. Prioritize the most actionable information. "
    "Keep the total length under 1500 characters."
)


def _fmt_stocks(stocks: Dict) -> str:
    if not stocks:
        return "  No data"
    lines = []
    for name, d in stocks.items():
        arrow = "▲" if d["change_pct"] >= 0 else "▼"
        lines.append(f"  {name}: ${d['price']} {arrow}{abs(d['change_pct']):.2f}%")
    return "\n".join(lines)


def _fmt_news(articles: List[str]) -> str:
    if not articles:
        return "  No articles"
    return "\n".join(f"  • {a}" for a in articles[:3])


def _fmt_emails(items: List[Dict]) -> str:
    if not items:
        return "  None"
    return "\n".join(
        f"  • \"{i.get('subject', '(no subject)')}\" — {i.get('from', '?')}"
        for i in items[:5]
    )


def _fmt_sms(items: List[Dict]) -> str:
    if not items:
        return "  None"
    return "\n".join(
        f"  • {i.get('from', '?')}: {i.get('body', '')[:60]}"
        for i in items[:5]
    )


def _fmt_teamworks(items: List[Dict]) -> str:
    if not items:
        return "  None"
    return "\n".join(
        f"  • {i.get('from', '?')}: {i.get('content', '')[:60]}"
        for i in items[:5]
    )


def compile_briefing(
    weather: Dict,
    news: Dict[str, List[str]],
    stocks: Dict,
    messages: Dict[str, List],
) -> str:
    tz = pytz.timezone(TIMEZONE)
    today = datetime.now(tz).strftime("%A, %B %d, %Y")

    user_content = f"""Compile a morning briefing for {today}.

WEATHER — {weather.get('city')}:
  Now: {weather.get('current_temp')}°F (feels {weather.get('feels_like')}°F), {weather.get('description')}
  High / Low: {weather.get('high')}°F / {weather.get('low')}°F
  Humidity: {weather.get('humidity')}%  Wind: {weather.get('wind_speed')} mph  Rain: {weather.get('precipitation_chance')}%

MARKET INDICES:
{_fmt_stocks(stocks.get('indices', {}))}

WATCHLIST:
{_fmt_stocks(stocks.get('watchlist', {}))}

BUSINESS NEWS:
{_fmt_news(news.get('business', []))}

MARKET NEWS:
{_fmt_news(news.get('markets', []))}

POLITICS / TOP NEWS:
{_fmt_news(news.get('politics', []))}

OVERNIGHT EMAILS ({len(messages.get('emails', []))} unread):
{_fmt_emails(messages.get('emails', []))}

OVERNIGHT SMS ({len(messages.get('sms', []))} received):
{_fmt_sms(messages.get('sms', []))}

TEAMWORKS MESSAGES ({len(messages.get('teamworks', []))} new):
{_fmt_teamworks(messages.get('teamworks', []))}

Write the SMS briefing now."""

    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=[
            {
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},  # cache the static system prompt
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    )

    return response.content[0].text
