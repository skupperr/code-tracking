import aiohttp
import asyncio
import re

class BaseResearchAPI:
    def __init__(self):
        self.session = aiohttp.ClientSession()  # Shared per instance

    async def close(self):
        await self.session.close()


    # backoff_factor	Waits 1s → 1.5s → 2.25s between tries
    async def get(self, url, params=None, headers=None, retries=3, backoff_factor=1.5, return_text=False):
        delay = 1
        for attempt in range(retries):
            try:
                async with self.session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        return await response.text() if return_text else await response.json()
                    else:
                        content = await response.text()
                        raise Exception(f"{self.__class__.__name__} Error {response.status}: {content}")
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                print(f"⚠️ Retry {attempt + 1}/{retries} for {url} due to error: {e}")
                await asyncio.sleep(delay)
                delay *= backoff_factor


    def clean_text(self, text):
        """Strips XML/HTML tags and normalizes whitespace."""
        if not text:
            return ''
        text = re.sub(r'<[^>]+>', '', text)
        return re.sub(r'\s+', ' ', text).strip()

    async def fetch(self, query, max_results=5):
        """Override in subclasses."""
        raise NotImplementedError("Each API class must implement fetch()")