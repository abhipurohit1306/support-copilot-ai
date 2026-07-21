
import asyncio

from app.chatbot import SupportChatbot
from app.embeddings import EmbeddingGenerator
from app.ingestion import IngestionService
from app.vector_store import VectorStore
from app.logger import logger



async def main():

    print("=" * 60)
    print("Support Copilot AI")
    print("=" * 60)

    ingestion = IngestionService()

    if ingestion.knowledge_base_exists():

        logger.info("Knowledge Base Found")
        logger.info("Loading existing knowledge base...")

    else:

        logger.warning("Knowledge Base not found.")
        logger.info("Creating knowledge base...")

        await ingestion.ingest_website(
            "https://docs.crawl4ai.com"
        )

    logger.info("Knowledge Base Ready!")

    # embedding_generator = EmbeddingGenerator()

    # vector_store = VectorStore(
    #     embedding_generator.embedding_model
    # )

    # print(f"\nDocuments in Chroma: {vector_store.count()}")

    chatbot = SupportChatbot(
        ingestion.vector_store
    )

    logger.info("Type 'exit' to quit.")

    while True:

        question = input("Ask Question > ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = chatbot.ask(question)

        print("\nAnswer:\n")
        print(answer)
        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())