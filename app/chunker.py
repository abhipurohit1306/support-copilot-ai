from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentChunker:

    def __init__(
        self,
        chunk_size=500,
        chunk_overlap=100,
    ):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk(self, text: str):

        return self.text_splitter.split_text(text)