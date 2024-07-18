import aiohttp
import asyncio
import logging
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GatewayService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def fetch_similar_titles(self, translated_title: str):
        url = f"{self.base_url}/compare/titles"
        payload = {'title': translated_title}
        logger.info(f"Sending request to {url} with payload: {payload}")

        timeout = aiohttp.ClientTimeout(total=120)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.post(url, json=payload) as response:
                    logger.info(f"Received response status: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        similar_titles = [item['similar_title'] for item in data]
                        logger.info(f"Received similar titles: {similar_titles}")
                        return similar_titles
                    else:
                        logger.error(f"Failed to fetch similar titles: {response.status}")
                        return []
            except asyncio.TimeoutError:
                logger.error("Request timed out")
                return []
            except aiohttp.ClientError as e:
                logger.error(f"Client error: {e}")
                return []


gateway_service = GatewayService(config.SIMILAR_TITLES_API_URL)
