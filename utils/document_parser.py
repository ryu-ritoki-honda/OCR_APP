import io
import fitz
from PIL import Image

from utils.models import DocumentPage


def parse_document(pdf_bytes):
    document = []

    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    try:
        for page_index in range(len(pdf)):
            page = pdf.load_page(page_index)

            # Extract digital text
            text = str(page.get_text("text")).strip()

            # Simple heuristic:
            # If very little text is found, this page probably needs OCR.
            needs_ocr = len(text) < 20

            # Render page as image
            pix = page.get_pixmap(dpi=300)

            image = Image.open(
                io.BytesIO(
                    pix.tobytes("png")
                )
            )

            document.append(
                DocumentPage(
                    page_number=page_index + 1,
                    digital_text=text,
                    image=image,
                    needs_ocr=needs_ocr
                )
            )
    finally:
        pdf.close()

    return document