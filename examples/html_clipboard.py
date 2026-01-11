"""Example: HTML clipboard operations."""

from xclipboard import Clipboard


def main():
    clipboard = Clipboard()
    
    # Set HTML content with plain text fallback
    html_content = "<h1>Hello, World!</h1><p>This is <strong>formatted</strong> text.</p>"
    plain_text_fallback = "Hello, World!\nThis is formatted text."
    
    clipboard.set_html(html_content, plain_text_fallback)
    print("HTML content set to clipboard")
    
    # Get HTML content
    retrieved_html = clipboard.get_html()
    print(f"Retrieved HTML: {retrieved_html}")
    
    # Get plain text (fallback)
    retrieved_text = clipboard.get_text()
    print(f"Retrieved text fallback: {retrieved_text}")
    
    # Check available formats
    formats = clipboard.get_available_formats()
    print(f"Available formats: {[f.name for f in formats]}")


if __name__ == "__main__":
    main()
