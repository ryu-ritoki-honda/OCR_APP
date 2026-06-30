from utils.models import DocumentPage


def merge_page(page: DocumentPage):

    digital = page.digital_text.strip()

    ocr = page.ocr_text.strip()

    sections = []

    if digital:
        sections.append(digital)

    if ocr:

        sections.append(
            "\n\n----- OCR CONTENT -----\n\n"
            + ocr
        )

    page.merged_text = "\n".join(sections)