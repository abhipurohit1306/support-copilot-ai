from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiLLM:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
        )

    def get_llm(self):
        return self.llm