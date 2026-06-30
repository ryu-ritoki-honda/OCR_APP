from utils.models import DocumentChunk


def chunk_document(pages):

    chunks = []

    for i, page in enumerate(pages):

        chunks.append(

            DocumentChunk(
                chunk_id=i,
                page_number=page.page_number,
                text=page.merged_text
            )

        )

    return chunks