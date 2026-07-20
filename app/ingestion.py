from app.crawler import WebsiteCrawler
from app.chunker import DocumentChunker
from app.embeddings import EmbeddingGenerator
from app.vector_store import VectorStore
from pathlib import Path


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
        """
        Checks whether a persisted ChromaDB knowledge base already exists.
        """

        chroma_path = Path("data/chroma_db")

        return chroma_path.exists() and any(chroma_path.iterdir())

    def __init__(self):

        self.crawler = WebsiteCrawler()

        self.chunker = DocumentChunker()

        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = VectorStore(
            self.embedding_generator.embedding_model
        )

    async def ingest_website(self, url: str):

        print("Step 1: Crawling Website...")

        pages = await self.crawler.crawl(url)

        print("Step 2: Chunking Documents...")

        documents = self.chunker.chunk(pages)

        print("Step 3: Storing in ChromaDB...")

        self.vector_store.add_documents(documents)

        print("Knowledge Base Created Successfully!")