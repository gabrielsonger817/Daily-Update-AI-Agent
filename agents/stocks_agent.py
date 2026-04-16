import yfinance as yf
from typing import Dict

from config import STOCK_WATCHLIST

_INDICES = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI",
    "VIX": "^VIX",
}


def _fetch_ticker(symbol: str) -> Dict | None:
    try:
        hist = yf.Ticker(symbol).history(period="2d")
        if len(hist) < 2:
            return None
        prev = hist["Close"].iloc[-2]
        last = hist["Close"].iloc[-1]
        pct = ((last - prev) / prev) * 100
        return {"price": round(last, 2), "change_pct": round(pct, 2)}
    except Exception:
        return None


def get_stock_data() -> Dict:
    indices = {}
    for name, ticker in _INDICES.items():
        result = _fetch_ticker(ticker)
        if result:
            indices[name] = result

    watchlist = {}
    for symbol in STOCK_WATCHLIST:
        result = _fetch_ticker(symbol)
        if result:
            watchlist[symbol] = result

    return {"indices": indices, "watchlist": watchlist}
