from utils.vector_store import VectorStore


class SearchService:

    def build(self, chunks):

        if not chunks:
            raise ValueError("No chunks provided.")

        if chunks[0].embedding is None:
            raise ValueError("Embeddings have not been generated.")

        dimension = len(chunks[0].embedding)

        store = VectorStore(dimension)

        store.add_embeddings(
            [chunk.embedding for chunk in chunks]
        )

        return store

    def search(
        self,
        store,
        question_embedding,
        k=8
    ):

        return store.search(
            question_embedding,
            k
        )