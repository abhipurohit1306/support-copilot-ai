from app.llm import GeminiLLM
from dotenv import load_dotenv
load_dotenv()

llm = GeminiLLM().get_llm()

response = llm.invoke("Say hello in one sentence.")

print(response.content)