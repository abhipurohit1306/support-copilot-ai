from langchain_core.output_parsers import StrOutputParser

from app.llm import GeminiLLM
from app.prompt import (
    SupportPrompt,
    QueryRewritePrompt,
)
from app.retriever import Retriever
from app.logger import logger


class SupportChatbot:
    """
    Coordinates the complete RAG pipeline.

    Conversation History
        ↓
    Query Rewriting
        ↓
    Retrieve
        ↓
    Prompt + Conversation History
        ↓
    LLM
        ↓
    Answer
    """

    def __init__(self, vector_store):

        self.retriever = Retriever(vector_store)

        self.prompt = SupportPrompt.get_prompt()

        self.query_rewrite_prompt = (
            QueryRewritePrompt.get_prompt()
        )

        self.llm = GeminiLLM().get_llm()

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

        self.query_rewrite_chain = (
            self.query_rewrite_prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(
        self,
        question: str,
        history: list[dict] | None = None,
    ):

        history = history or []

        # --------------------------------------------------
        # 1. Rewrite follow-up question
        # --------------------------------------------------

        if history:

            history_text = "\n".join(
                f"{message['role'].capitalize()}: "
                f"{message['content']}"
                for message in history
            )

            logger.info("=" * 60)
            logger.info("Conversation History:")
            logger.info("%s", history_text)
            logger.info("=" * 60)

            retrieval_query = (
                self.query_rewrite_chain.invoke(
                    {
                        "history": history_text,
                        "question": question,
                    }
                )
            ).strip()

        else:

            retrieval_query = question

        logger.info(
            "Retrieval Query: %s",
            retrieval_query,
        )

        # --------------------------------------------------
        # 2. Retrieve using standalone question
        # --------------------------------------------------

        results = self.retriever.retrieve(
            retrieval_query
        )

        scores = [
            item["score"]
            for item in results
        ]

        documents = [
            item["document"]
            for item in results
        ]

        # --------------------------------------------------
        # 3. Build source information
        # --------------------------------------------------

        sources = []

        for item in results:

            sources.append(
            {
                "title": item["metadata"].get("title", ""),
                "source": item["metadata"].get("source", ""),
                "score": item["score"],
            }
        )

        unique_sources = []

        seen = set()

        for source in sources:

            url = source["source"]

            if url not in seen:

                unique_sources.append(source)

                seen.add(url)

        # --------------------------------------------------
        # 4. Log retrieved documents
        # --------------------------------------------------

        logger.debug("=" * 60)

        logger.debug(
            "Retrieved %d document(s)",
            len(documents),
        )

        for i, doc in enumerate(
            documents,
            start=1,
        ):

            logger.debug(
                "Document %d",
                i,
            )

            logger.debug("-" * 40)

            logger.debug(
                doc.page_content[:500]
            )

        # --------------------------------------------------
        # 5. Build context
        # --------------------------------------------------

        context = "\n\n".join(
            item["content"]
            for item in results
        )

        # --------------------------------------------------
        # 6. Build conversation history
        # --------------------------------------------------

        history_text = "\n".join(
            f"{message['role'].capitalize()}: "
            f"{message['content']}"
            for message in history
        )

        if history_text:

            question_with_history = (
                "Conversation history:\n"
                f"{history_text}\n\n"
                "Current user question:\n"
                f"{question}"
            )

        else:

            question_with_history = question

        # --------------------------------------------------
        # 7. Generate answer
        # --------------------------------------------------

        answer = self.chain.invoke(
            {
                "question": question_with_history,
                "context": context,
            }
        )

        best_score = (
            min(scores)
            if scores
            else None
        )

        logger.info(
            "Answer generated. Best Score: %s",
            best_score,
        )

        return {
            "answer": answer,
            "sources": unique_sources,
            "best_score": best_score,
        }