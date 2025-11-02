from PIL import Image
import pytesseract


def extract_text(image_path: str) -> str:
    """
    Extract text from an image using pytesseract.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted text (stripped of leading/trailing whitespace).
    """
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

