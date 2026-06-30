from utils.document_parser import parse_document
from utils.models import PipelineResult
from utils.preprocess import preprocess_image
from utils.ocr import run_ocr
from utils.document_merger import merge_page
from utils.document_builder import build_document
from utils.chunker import chunk_document
from utils.azure_embeddings import create_embedding


def process_document(pdf_bytes):

    pages = parse_document(pdf_bytes)

    for page in pages:
        page.processed_image = preprocess_image(page.image)
        page.ocr_text = run_ocr(page.processed_image)
        merge_page(page)

    document = build_document(pages)

    chunks = chunk_document(pages)

    return PipelineResult(
        pages=pages,
        document=document,
        chunks=chunks
    )


def generate_embeddings(chunks):

    for chunk in chunks:
        chunk.embedding = create_embedding(chunk.text)