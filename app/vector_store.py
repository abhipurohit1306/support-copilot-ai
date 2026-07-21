from langchain_chroma import Chroma


class VectorStore:

    def __init__(self, embedding_model):

        self.vector_db = Chroma(
            collection_name="support_copilot",
            embedding_function=embedding_model,
            persist_directory="data/chroma_db",
        )

    def add_documents(self, documents):

        self.vector_db.add_documents(documents)

    def similarity_search(self, query, k=3):

        return self.vector_db.similarity_search(
            query=query,
            k=k,
        )

    def count(self):

        return self.vector_db._collection.count()