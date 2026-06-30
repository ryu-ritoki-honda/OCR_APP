from utils.document_parser import parse_document
from utils.preprocess import preprocess_image
from utils.ocr import run_ocr
from utils.document_merger import merge_page
from utils.document_builder import build_document
from utils.chunker import chunk_document
from utils.models import PipelineResult


class DocumentService:

    def process(self, pdf_bytes):

        pages = parse_document(pdf_bytes)

        for page in pages:

            page.processed_image = preprocess_image(page.image)

            page.ocr_text = run_ocr(page.processed_image)

            merge_page(page)

        document = build_document(pages)

        chunks = chunk_document(
            pages,
            filename="Uploaded PDF"
        )

        return PipelineResult(
            pages=pages,
            document=document,
            chunks=chunks
        )