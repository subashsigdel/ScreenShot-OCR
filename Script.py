import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
import pytesseract
import pyperclip  # ← required for clipboard operations


def extract_text(image_path: str) -> str:
    """
    Extract text from an image using pytesseract.
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
    """
    if text:
        pyperclip.copy(text)
        print("Copied to clipboard:")
        print(text)
    else:
        print("No text to copy.")


WATCH_FOLDER = "/home/subash/vs/ScreenShot-OCR/Images/Screenshots"


class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggered when a new file is created in the folder."""
        if event.is_directory:
            return

        if not event.src_path.lower().endswith((".png", ".jpg", ".jpeg")):
            return

        # Wait to ensure the screenshot file is saved completely
        time.sleep(1)
        print(f"New screenshot detected: {event.src_path}")
        self.process_image(event.src_path)

    @staticmethod
    def process_image(filepath):
        """Extract text from the image and copy it to clipboard."""
        text = extract_text(filepath)
        if text:
            print("Extracted Text:\n", text)
            copy_to_clipboard(text)
            print("Text copied to clipboard!")
        else:
            print("No text found in image.")


if __name__ == "__main__":
    print(f"Watching folder: {WATCH_FOLDER} for new screenshots...")

    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
