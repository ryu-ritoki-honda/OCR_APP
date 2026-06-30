from openai import AzureOpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_API_VERSION,
    EMBEDDING_MODEL
)

client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT, # type: ignore
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
)


def create_embedding(text: str) -> list[float]:

    response = client.embeddings.create(
        model=EMBEDDING_MODEL, # type: ignore
        input=text
    )

    return response.data[0].embedding