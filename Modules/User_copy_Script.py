import pyperclip

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




