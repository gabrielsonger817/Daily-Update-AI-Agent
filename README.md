# Daily Update AI Agent

Sends a personalized morning briefing to your phone via SMS every day at 8:45 AM, compiled by Claude. Covers weather, stock market, business/politics news, and any messages you received overnight (email, SMS, Teamworks).

## What's included in each briefing

| Section | Source |
|---------|--------|
| 🌤 Weather | OpenWeatherMap |
| 📈 Market indices (S&P 500, Nasdaq, Dow, VIX) | Yahoo Finance (yfinance) |
| 📊 Your stock watchlist | Yahoo Finance (yfinance) |
| 📰 Business, markets & politics headlines | NewsAPI |
| 📧 Overnight unread emails | Gmail / IMAP |
| 💬 Overnight SMS received | Twilio |
| 🏟 Teamworks messages | Teamworks API |

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys (see table below).

### 3. Set your stock watchlist

In `.env`, set `STOCK_WATCHLIST` to a comma-separated list of tickers:

```
STOCK_WATCHLIST=SPY,QQQ,AAPL,NVDA,TSLA
```

### 4. Run

**Test immediately (no scheduling):**
```bash
python main.py --now
```

**Start the daily scheduler (keeps running, fires at 8:45 AM):**
```bash
python main.py
```

For production, run this as a persistent background service (e.g. `systemd`, `pm2`, or a screen session on a VPS/Raspberry Pi).

## Required API Keys

| Service | Where to get it | Used for |
|---------|----------------|----------|
| [Anthropic](https://console.anthropic.com) | `ANTHROPIC_API_KEY` | Compiling the briefing |
| [Twilio](https://www.twilio.com/console) | `TWILIO_*` | Sending & receiving SMS |
| [NewsAPI](https://newsapi.org) | `NEWS_API_KEY` | Headlines |
| [OpenWeatherMap](https://openweathermap.org/api) | `OPENWEATHER_API_KEY` | Weather |
| Gmail | App Password via [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) | Overnight emails |
| Teamworks | Contact developer@teamworksathletics.com | Team messages |

## Notes

- **Received SMS**: Works only if people are texting your Twilio number. If you want to forward your personal number's texts, configure an SMS forwarding rule in your carrier settings or use an app like Google Messages (Android) or an iOS Shortcut to relay overnight messages to your Twilio number.
- **Teamworks API**: Teamworks does not publish a fully open REST API. You will need to contact their support team for official API documentation and credentials. The endpoint in `services/teamworks_service.py` may need adjustment.
- **Gmail App Password**: Do **not** use your real Gmail password. Generate an App Password in your Google account security settings.

## Project structure

```
├── main.py                      # Entry point
├── scheduler.py                 # APScheduler cron trigger
├── config.py                    # Centralised env-var config
├── agents/
│   ├── news_agent.py            # NewsAPI headlines
│   ├── weather_agent.py         # OpenWeatherMap forecast
│   ├── stocks_agent.py          # yfinance market data
│   ├── messages_agent.py        # Aggregates all message sources
│   └── briefing_agent.py        # Claude API — compiles final SMS
└── services/
    ├── sms_service.py           # Twilio send + receive
    ├── email_service.py         # Gmail IMAP
    └── teamworks_service.py     # Teamworks REST API
```
