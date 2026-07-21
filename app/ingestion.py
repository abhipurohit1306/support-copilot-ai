from app.crawler import WebsiteCrawler
from app.chunker import DocumentChunker
from app.embeddings import EmbeddingGenerator
from app.vector_store import VectorStore
from pathlib import Path
from app.logger import logger


class IngestionService:
    """
    Coordinates the knowledge base creation pipeline.

    Crawl
        ↓
    Chunk
        ↓
    Store in ChromaDB
    """
    def knowledge_base_exists(self) -> bool:
        return self.vector_store.count() > 0
    

    def __init__(self):

        self.crawler = WebsiteCrawler()

        self.chunker = DocumentChunker()

        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = VectorStore(
            self.embedding_generator.embedding_model
        )

    async def ingest_website(self, url: str):

        logger.info("Step 1: Crawling Website...")

        pages = await self.crawler.crawl(url)

        logger.debug("Pages type: %s", type(pages))
        logger.info("Pages crawled: %d", len(pages))

        logger.info("Step 2: Chunking Documents...")

        documents = self.chunker.chunk(pages)

        logger.info("Chunks created: %d", len(documents))

        logger.info("Step 3: Storing in ChromaDB...")

        self.vector_store.add_documents(documents)

        logger.info(
            "Documents indexed: %d",
            self.vector_store.count()
        )

        logger.info("Knowledge Base Created Successfully!")