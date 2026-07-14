from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingGenerator:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_documents(self, chunks):

        return self.embedding_model.embed_documents(chunks)

    def embed_query(self, query):

        return self.embedding_model.embed_query(query)