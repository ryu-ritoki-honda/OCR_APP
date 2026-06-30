from utils.models import DocumentChunk


CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def chunk_document(
    pages,
    filename="Unknown"
):

    chunks = []

    chunk_id = 0

    for page in pages:

        text = page.merged_text.strip()

        if not text:
            continue

        start = 0

        while start < len(text):

            end = min(
                start + CHUNK_SIZE,
                len(text)
            )

            chunk_text = text[start:end]

            chunks.append(

                DocumentChunk(

                    id=chunk_id,

                    page_number=page.page_number,

                    filename=filename,

                    title="",

                    source=f"Page {page.page_number}",

                    text=chunk_text

                )

            )

            chunk_id += 1

            if end == len(text):
                break

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks