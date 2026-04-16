from newsapi import NewsApiClient
from datetime import datetime, timedelta
from typing import Dict, List

from config import NEWS_API_KEY


def get_top_news() -> Dict[str, List[str]]:
    api = NewsApiClient(api_key=NEWS_API_KEY)
    since = (datetime.utcnow() - timedelta(hours=24)).isoformat()

    def _headlines(category: str) -> List[str]:
        resp = api.get_top_headlines(
            category=category, language="en", country="us", page_size=5
        )
        return [a["title"] for a in resp.get("articles", [])[:5]]

    def _everything(query: str) -> List[str]:
        resp = api.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            from_param=since,
            page_size=5,
        )
        return [a["title"] for a in resp.get("articles", [])[:5]]

    return {
        "business": _headlines("business"),
        "politics": _headlines("general"),
        "markets": _everything("stock market OR S&P 500 OR nasdaq OR dow jones"),
    }
