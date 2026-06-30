import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings):

        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        self.index.add(vectors)

    def search(self, embedding, k=8):

        query = np.array(
            [embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query,
            k
        )

        return indices[0], distances[0]