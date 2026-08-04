from langchain_core.output_parsers import StrOutputParser

from app.llm import GeminiLLM
from app.prompt import SupportPrompt
from app.retriever import Retriever
from app.logger import logger


class SupportChatbot:
    """
    Coordinates the complete RAG pipeline.

    Question
        ↓
    Retrieve
        ↓
    Prompt
        ↓
    LLM
        ↓
    Answer
    """

    def __init__(self, vector_store):

        self.retriever = Retriever(vector_store)

        self.prompt = SupportPrompt.get_prompt()

        self.llm = GeminiLLM().get_llm()

        self.chain = ( 
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question):

        results = self.retriever.retrieve(question)

        scores = [
            item["score"]
            for item in results
        ]

        documents = [
            item["document"]
            for item in results
        ]

        logger.debug("=" * 60)
        logger.debug("Retrieved %d document(s)", len(documents))

        for i, doc in enumerate(documents, start=1):
            logger.debug("Document %d", i)
            logger.debug("-" * 40)
            logger.debug(doc.page_content[:500])

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        answer = self.chain.invoke(
            {
                "question": question,
                "context": context,
            }
        )
        
        return {
            "answer": answer,
            "documents": documents,
            "scores": scores,
            "best_score": min(scores) if scores else None,
        }