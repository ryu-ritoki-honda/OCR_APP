from utils.models import DocumentPage


def build_document(pages):

    document = []

    for page in pages:

        document.append(

            f"""
========================
PAGE {page.page_number}
========================

{page.merged_text}
"""
        )

    return "\n".join(document)