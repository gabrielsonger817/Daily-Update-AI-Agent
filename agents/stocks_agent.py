import yfinance as yf
from typing import Dict

from config import STOCK_WATCHLIST

_INDICES = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI",
    "VIX": "^VIX",
}

# One-word industry/category label for each watchlist ticker
_LABELS: Dict[str, str] = {
    "NVDA":  "Semiconductors",
    "MSFT":  "Software",
    "GOOGL": "Tech",
    "TSM":   "Semiconductors",
    "AVGO":  "Semiconductors",
    "WELL":  "Healthcare REIT",
    "PLD":   "Logistics REIT",
    "AMT":   "Tower REIT",
    "BX":    "Private Equity",
    "APO":   "Private Equity",
    "KKR":   "Private Equity",
    "JPM":   "Banking",
    "BAC":   "Banking",
    "WFC":   "Banking",
    "CAT":   "Industrials",
    "BIP":   "Infrastructure",
    "NEE":   "Utilities",
    "XOM":   "Energy",
    "CVX":   "Energy",
    "COP":   "Energy",
    "NEM":   "Gold Mining",
    "AEM":   "Gold Mining",
    "FNV":   "Gold Royalties",
    "WPM":   "Silver Royalties",
    "MSTR":  "Bitcoin",
    "COIN":  "Crypto Exchange",
    "TSLA":  "EV",
    "TM":    "Auto",
    "GM":    "Auto",
    "IBIT":  "Bitcoin ETF",
    "VOO":   "S&P 500 ETF",
    "VTWO":  "Russell 2000 ETF",
    "QQQM":  "Nasdaq ETF",
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
            result["label"] = _LABELS.get(symbol, "")
            watchlist[symbol] = result

    return {"indices": indices, "watchlist": watchlist}
