import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from User_copy_Script import copy_to_clipboard  

# User configuration
USER = "subash"
WATCH_FOLDER = "/home/subash/vs/ScreenShot-OCR/Images/Screenshots"
API_URL_UPLOAD = "http://127.0.0.1:8000/upload/"


class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Called when a new file is created in the watched folder."""
        if event.is_directory:
            return

        if not event.src_path.lower().endswith((".png", ".jpg", ".jpeg")):
            return
            # Wait a bit to ensure file is fully written
        time.sleep(1)
        print(f"New screenshot detected: {event.src_path}")
        self.send_to_api(event.src_path)

    def send_to_api(self, filepath):
        """Send the new screenshot to the FastAPI OCR endpoint."""
        with open(filepath, "rb") as f:
            files = {"file": (os.path.basename(filepath), f)}
            data = {"username": USER}
            try:
                response = requests.post(API_URL_UPLOAD, files=files, data=data)
                if response.status_code == 200:
                    result = response.json()
                    print("OCR Text:", result["text"])
                    # Automatically copy extracted text to clipboard
                    self.copy_text_to_clipboard(result["text"])
                else:
                    print("Error uploading:", response.status_code, response.text)
            except Exception as e:
                print("Failed to send to API:", e)

    @staticmethod
    def get_text_api(user: str, filename: str):
        """
        Fetch OCR text for a given username and uploaded filename.
        """
        saved_filename = f"{user}_{filename}"
        url = f"http://127.0.0.1:8000/text/{saved_filename}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print("Extracted text:", data["text"])
                copy_to_clipboard(data["text"])
                return data["text"]
            else:
                print("Error:", response.status_code, response.text)
                return None
        except Exception as e:
            print("Request failed:", e)
            return None

    @staticmethod
    def copy_text_to_clipboard(text: str):
        """Copy text to clipboard using your helper."""
        try:
            copy_to_clipboard(text)
            print("Text copied to clipboard!")
        except Exception as e:
            print("Failed to copy to clipboard:", e)


if __name__ == "__main__":
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"Watching folder: {WATCH_FOLDER} for new screenshots...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
