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