import pytesseract

from utils.preprocess import preprocess_image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def run_ocr(image):

    config = r'--oem 3 --psm 6'

    return pytesseract.image_to_string(
        image,
        lang="eng+jpn",
        config=config
    ).strip()