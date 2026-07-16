import asyncio

from app.crawler import WebsiteCrawler
from app.chunker import DocumentChunker
from app.embeddings import EmbeddingGenerator
from app.vector_store import VectorStore
from app.retriever import Retriever


async def main():

    # Crawl
    crawler = WebsiteCrawler()
    result = await crawler.crawl("https://docs.crawl4ai.com")

    # Chunk
    chunker = DocumentChunker()

    metadata = {
        "source": result.url,
        "title": result.metadata.get("title", "Unknown")
    }

    documents = chunker.chunk(
        result.markdown,
        metadata
    )

    # Vector Store
    embedding = EmbeddingGenerator()

    vector_store = VectorStore(
        embedding.embedding_model
    )

    vector_store.add_documents(documents)

    # Retriever
    retriever = Retriever(vector_store)

    query = "How do I install Crawl4AI?"

    results = retriever.retrieve(query)

    print(f"\nQuery: {query}\n")

    for index, doc in enumerate(results, start=1):

        print("=" * 80)
        print(f"Result {index}")
        print("=" * 80)

        print(doc.page_content[:500])
        print()

if __name__ == "__main__":
    asyncio.run(main())