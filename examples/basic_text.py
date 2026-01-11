"""Example: Basic text clipboard operations."""

from xclipboard import Clipboard


def main():
    clipboard = Clipboard()
    
    # Set plain text
    clipboard.set_text("Hello, XClipboard!")
    print("Text set to clipboard")
    
    # Get plain text
    text = clipboard.get_text()
    print(f"Retrieved text: {text}")
    
    # Check available formats
    formats = clipboard.get_available_formats()
    print(f"Available formats: {[f.name for f in formats]}")
    
    # Check if clipboard is empty
    print(f"Clipboard is empty: {clipboard.is_empty()}")
    
    # Clear clipboard
    clipboard.clear()
    print("Clipboard cleared")
    print(f"Clipboard is empty after clear: {clipboard.is_empty()}")


if __name__ == "__main__":
    main()
