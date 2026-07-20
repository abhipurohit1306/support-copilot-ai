from langchain_core.documents import Document
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

    def chunk(self, crawl_results):

        documents = []

        for result in crawl_results:

            # Skip failed pages
            if not result.success:
                continue

            # Skip empty pages
            if not result.markdown:
                continue

            chunks = self.text_splitter.split_text(result.markdown)

            for chunk in chunks:

                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "source": result.url,
                            "title": getattr(result, "title", ""),
                        },
                    )
                )

        return documents