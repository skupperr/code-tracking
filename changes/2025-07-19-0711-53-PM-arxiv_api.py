from .base_api import BaseResearchAPI
import aiohttp
import feedparser
import re


class ArxivAPI(BaseResearchAPI):
    async def fetch(self, query, max_results=15):
        base_url = 'http://export.arxiv.org/api/query'
        search_query = f'all:{query}'
        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results
        }

        try:
            text_data = await self.get(base_url, params=params)
            parsed = feedparser.parse(text_data if isinstance(text_data, str) else str(text_data))
        except Exception as e:
            print(f"⚠️ ArxivAPI failed: {e}")
            return []

        results = []
        for entry in parsed.entries:
            results.append({
                "title": entry.title,
                "summary": self.clean_text(entry.summary),
                "authors": [author.name for author in entry.authors],
                "doi": entry.link,
                "year": entry.published[:4],
                "web_link": entry.link,
                "score": None,
                "source": "Arxiv"
            })

        return results