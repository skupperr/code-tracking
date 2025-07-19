import aiohttp
import xmltodict
import re

from .base_api import BaseResearchAPI


class PubMedAPI(BaseResearchAPI):
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    def clean_abstract(self, text):
        if not text:
            return ""
        return re.sub(r"\s+", " ", text).strip()

    async def fetch(self, query, max_results=5):
        # Step 1: Search PubMed for article IDs
        search_params = {
            "db": "pubmed",
            "retmode": "json",
            "retmax": max_results,
            "term": query
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=search_params) as response:
                    ids_data = await response.json()

                id_list = ids_data.get("esearchresult", {}).get("idlist", [])
                if not id_list:
                    return []

                # Step 2: Fetch article metadata by IDs
                fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
                fetch_params = {
                    "db": "pubmed",
                    "id": ",".join(id_list),
                    "retmode": "xml"
                }

                async with session.get(fetch_url, params=fetch_params) as fetch_response:
                    xml_data = await fetch_response.text()
                    parsed = xmltodict.parse(xml_data)

        except Exception as e:
            print(f"⚠️ PubMedAPI failed: {e}")
            return []

        articles = parsed.get("PubmedArticleSet", {}).get("PubmedArticle", [])
... (truncated for brevity)