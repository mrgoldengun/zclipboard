"""Example: Using ClipboardData for flexible clipboard operations."""

from xclipboard import Clipboard, ClipboardFormat
from xclipboard.data_types import ClipboardData


def main():
    clipboard = Clipboard()
    
    # Create ClipboardData objects
    text_data = ClipboardData("Hello from ClipboardData!", ClipboardFormat.PLAIN_TEXT)
    print(f"Created: {text_data}")
    
    # Set using ClipboardData
    clipboard.set(text_data)
    print("Text set using ClipboardData")
    
    # Get data with automatic format detection
    retrieved = clipboard.get()
    if retrieved:
        print(f"Retrieved: {retrieved}")
        print(f"Format: {retrieved.format_type.name}")
        print(f"Data: {retrieved.data}")
    
    # Get data in specific format
    text_retrieved = clipboard.get(ClipboardFormat.PLAIN_TEXT)
    if text_retrieved:
        print(f"Specifically retrieved text: {text_retrieved.data}")
    
    # HTML example with ClipboardData
    html_data = ClipboardData(
        "<p>Hello <strong>World</strong></p>",
        ClipboardFormat.HTML
    )
    clipboard.set(html_data, plain_text_fallback="Hello World")
    print("HTML set using ClipboardData with fallback")
    
    # List all available formats
    print("\nAvailable formats on clipboard:")
    for fmt in clipboard.get_available_formats():
        print(f"  - {fmt.name}")


if __name__ == "__main__":
    main()
