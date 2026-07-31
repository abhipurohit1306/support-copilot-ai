from app.embeddings import EmbeddingGenerator
from app.vector_store import VectorStore
from app.chatbot import SupportChatbot

embedding_model = EmbeddingGenerator().get_embedding_model()

vector_store = VectorStore(embedding_model)

chatbot = SupportChatbot(vector_store)