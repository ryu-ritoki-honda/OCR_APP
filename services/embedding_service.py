from utils.azure_embeddings import create_embedding


class EmbeddingService:

    def generate(self, chunks):

        for chunk in chunks:

            if chunk.embedding is None:

                chunk.embedding = create_embedding(
                    chunk.text
                )