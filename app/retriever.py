from app.config import TOP_K
from app.logger import logger

class Retriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store

    def retrieve(self, query: str,):
        results = self.vector_store.similarity_search(
            query=query,
            k=TOP_K,
        )
        logger.info("=" * 60)
        logger.info("Retrieval Results")
        logger.info("Query: %s", query)
        logger.info("Retrieved %d document(s)", len(results))

        for index, (document, score) in enumerate(results, start=1):

            logger.info("-" * 40)

            logger.info("Rank   : %d", index)

            logger.info("Score  : %.4f", score)

            logger.info(
                "Source : %s",
                document.metadata.get("source", "Unknown"),
            )

            logger.info(
                "Title  : %s",
                document.metadata.get("title", "Unknown"),
            )

            logger.debug(
                "Content:\n%s",
                document.page_content[:300],
            )




        return [
            {
                "document": document,
                "content": document.page_content,
                "metadata": document.metadata,
                "score": score,
            }
            for document, score in results
        ]
        