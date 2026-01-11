"""Example: Creating a custom clipboard backend."""

from typing import List, Optional

from xclipboard import Clipboard, ClipboardFormat
from xclipboard.backends.base import ClipboardBackend


class InMemoryClipboardBackend(ClipboardBackend):
    """
    A simple in-memory clipboard backend for testing or special use cases.
    Demonstrates how to create custom backends.
    """
    
    def __init__(self):
        self._storage = {}
    
    def clear(self) -> None:
        self._storage.clear()
    
    def get_available_formats(self) -> List[ClipboardFormat]:
        return list(self._storage.keys())
    
    def get_html(self) -> Optional[str]:
        return self._storage.get(ClipboardFormat.HTML)
    
    def get_image(self) -> Optional[bytes]:
        return self._storage.get(ClipboardFormat.IMAGE)
    
    def get_rtf(self) -> Optional[str]:
        return self._storage.get(ClipboardFormat.RTF)
    
    def get_text(self) -> Optional[str]:
        return self._storage.get(ClipboardFormat.PLAIN_TEXT)
    
    def set_html(self, html_content: str, plain_text_fallback: Optional[str] = None) -> None:
        self._storage.clear()
        self._storage[ClipboardFormat.HTML] = html_content
        if plain_text_fallback:
            self._storage[ClipboardFormat.PLAIN_TEXT] = plain_text_fallback
    
    def set_image(self, image_data: bytes) -> None:
        self._storage.clear()
        self._storage[ClipboardFormat.IMAGE] = image_data
    
    def set_rtf(self, rtf_content: str, plain_text_fallback: Optional[str] = None) -> None:
        self._storage.clear()
        self._storage[ClipboardFormat.RTF] = rtf_content
        if plain_text_fallback:
            self._storage[ClipboardFormat.PLAIN_TEXT] = plain_text_fallback
    
    def set_text(self, text: str) -> None:
        self._storage.clear()
        self._storage[ClipboardFormat.PLAIN_TEXT] = text


def main():
    # Create clipboard with custom backend
    custom_backend = InMemoryClipboardBackend()
    clipboard = Clipboard(backend=custom_backend)
    
    # Use clipboard normally
    clipboard.set_text("Hello from custom backend!")
    print(f"Text: {clipboard.get_text()}")
    
    clipboard.set_html("<b>Bold</b>", "Bold")
    print(f"HTML: {clipboard.get_html()}")
    print(f"Text fallback: {clipboard.get_text()}")
    
    # Access backend directly if needed
    print(f"Backend type: {type(clipboard.backend).__name__}")
    print(f"Available formats: {[f.name for f in clipboard.get_available_formats()]}")


if __name__ == "__main__":
    main()
