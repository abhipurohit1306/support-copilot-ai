from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

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
            {
                "context": RunnableLambda(self._retrieve_context),
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    # def _retrieve_context(self, question: str):

    #     documents = self.retriever.retrieve(question)

    #     return "\n\n".join(
    #         document.page_content
    #         for document in documents
    #     )

    def _retrieve_context(self, question: str):

        documents = self.retriever.retrieve(question)

        logger.debug("=" * 60)
        logger.debug("Retrieved %d document(s)", len(documents))

        for i, doc in enumerate(documents, start=1):
            logger.debug("Document %d", i)
            logger.debug("-" * 40)
            logger.debug(doc.page_content[:500])

        return "\n\n".join(
            document.page_content
            for document in documents
        )

    def ask(self, question: str):
        return self.chain.invoke(question)