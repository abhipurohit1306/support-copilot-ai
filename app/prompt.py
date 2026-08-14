from langchain_core.prompts import ChatPromptTemplate


class SupportPrompt:

    @staticmethod
    def get_prompt():

        return ChatPromptTemplate.from_template(
            """
            You are Support Copilot AI.
            You are answering customer support questions.
            Use ONLY the provided context.
            If the answer cannot be found in the context, reply:
            "I couldn't find that information in the documentation."
            Do not make up information.
            Context: {context}
            Question: {question}
            Answer:
            """
        )


class QueryRewritePrompt:

    @staticmethod
    def get_prompt():

        return ChatPromptTemplate.from_template(
            """
            Rewrite the user's current question into a standalone
            question that can be understood without conversation history.

            Use the conversation history only to resolve references
            such as "it", "they", "this", "that", or "the above".

            Do not answer the question.
            Return ONLY the rewritten standalone question.

            Conversation History:
            {history}

            Current Question:
            {question}

            Standalone Question:
            """
        )