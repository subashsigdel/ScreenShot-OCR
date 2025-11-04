# AIzaSyBs08nEvWUWMkAKSn-6AO5LdSaAqTQN2gg

from google.cloud import vision
import io

def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        print("Detected text:")
        print(texts[0].description)
    else:
        print("No text detected.")

    if response.error.message:
        raise Exception(f"{response.error.message}")

# Example usage
detect_text("sample_image.png")
