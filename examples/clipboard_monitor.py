"""Example: Monitor clipboard for changes."""

import time
from typing import Optional

from xclipboard import Clipboard, ClipboardFormat


def get_clipboard_signature(clipboard: Clipboard) -> Optional[str]:
    """Get a simple signature of current clipboard content."""
    text = clipboard.get_text()
    if text:
        return f"text:{hash(text)}"
    
    image = clipboard.get_image()
    if image:
        return f"image:{hash(image)}"
    
    return None


def main():
    clipboard = Clipboard()
    print("Clipboard monitor started. Press Ctrl+C to stop.")
    print("Copy something to see changes!\n")
    
    last_signature = get_clipboard_signature(clipboard)
    
    try:
        while True:
            current_signature = get_clipboard_signature(clipboard)
            
            if current_signature != last_signature:
                print(f"[{time.strftime('%H:%M:%S')}] Clipboard changed!")
                
                formats = clipboard.get_available_formats()
                print(f"  Available formats: {[f.name for f in formats]}")
                
                if ClipboardFormat.PLAIN_TEXT in formats:
                    text = clipboard.get_text()
                    preview = text[:50] + "..." if text and len(text) > 50 else text
                    print(f"  Text preview: {preview}")
                
                if ClipboardFormat.IMAGE in formats:
                    image = clipboard.get_image()
                    if image:
                        print(f"  Image size: {len(image)} bytes")
                
                print()
                last_signature = current_signature
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\nMonitor stopped.")


if __name__ == "__main__":
    main()
