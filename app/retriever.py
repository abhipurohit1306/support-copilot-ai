class Retriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        k: int = 3
    ):

        return self.vector_store.similarity_search(
            query=query,
            k=k
        )