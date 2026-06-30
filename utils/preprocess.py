import cv2
import numpy as np
from PIL import Image


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess an image to improve OCR accuracy.
    """

    # Convert PIL -> OpenCV
    img = np.array(image)

    # Convert RGB -> Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Enlarge image (helps small text)
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Reduce noise
    gray = cv2.medianBlur(gray, 3)

    # Increase contrast using adaptive threshold
    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    # Convert back to PIL
    return Image.fromarray(gray)