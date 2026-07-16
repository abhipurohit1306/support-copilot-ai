import asyncio

from app.crawler import WebsiteCrawler
from app.chunker import DocumentChunker
from app.embeddings import EmbeddingGenerator
from app.vector_store import VectorStore
from app.retriever import Retriever


async def main():

    crawler = WebsiteCrawler()

    crawl_results = await crawler.crawl(
        "https://docs.crawl4ai.com"
    )

    chunker = DocumentChunker()

    all_documents = []

    for result in crawl_results:

        metadata = {
            "source": result.url,
            "title": result.metadata.get("title", "Unknown")
        }

        documents = chunker.chunk(
            text=result.markdown,
            metadata=metadata
        )

        all_documents.extend(documents)

    print(f"\nTotal Chunks : {len(all_documents)}")

    embedding = EmbeddingGenerator()

    vector_store = VectorStore(
        embedding.embedding_model
    )

    vector_store.add_documents(all_documents)

    retriever = Retriever(vector_store)

    query = "How do I install Crawl4AI?"

    results = retriever.retrieve(query)

    print(f"\nQuery : {query}\n")

    for index, doc in enumerate(results, start=1):

        print("=" * 100)
        print(f"Result {index}")
        print("=" * 100)

        print("TITLE :", doc.metadata.get("title"))
        print("SOURCE:", doc.metadata.get("source"))
        print()

        print(doc.page_content[:1000])
        print()

if __name__ == "__main__":
    asyncio.run(main())