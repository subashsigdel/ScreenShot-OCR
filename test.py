from PIL import Image
import pytesseract
import pyperclip

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

def copy_to_clipboard(text: str) -> None:
    """
    Copy the given text to the system clipboard.

    Args:
        text (str): Text to copy.
    """
    if text:
        pyperclip.copy(text)
        print("Copied to clipboard:")
        print(text)
    else:
        print("No text to copy.")

if __name__ == "__main__":
    # Example usage
    image_path = "new.png"
    text = extract_text(image_path)
    copy_to_clipboard(text)
