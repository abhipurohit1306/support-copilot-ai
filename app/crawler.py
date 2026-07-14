from crawl4ai import AsyncWebCrawler


class WebsiteCrawler:

    async def crawl(self, url: str):
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)

            if not result.success:
                raise Exception(f"Failed to crawl: {url}")

        return result