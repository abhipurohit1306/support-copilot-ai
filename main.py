import asyncio

from app.ingestion import IngestionService


async def main():

    print("=" * 50)
    print("Support Copilot AI")
    print("=" * 50)

    ingestion = IngestionService()

    if ingestion.knowledge_base_exists():

        print("\nKnowledge Base Found")
        print("Loading existing knowledge base...")

    else:

        print("\nKnowledge Base not found.")
        print("Creating knowledge base...\n")

        await ingestion.ingest_website(
            "https://docs.crawl4ai.com"
        )

    print("\nKnowledge Base Ready!")


if __name__ == "__main__":
    asyncio.run(main())