from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
)

from crawl4ai.deep_crawling import BFSDeepCrawlStrategy


class WebsiteCrawler:
    """
    Crawls a documentation website using
    Crawl4AI's built-in BFS deep crawler.
    """

    async def crawl(self, url: str):

        config = CrawlerRunConfig(
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=2,
                max_pages=30,
                include_external=False,
            )
        )

        async with AsyncWebCrawler() as crawler:

            results = await crawler.arun(
                url=url,
                config=config,
            )

        return results