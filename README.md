# XClipboard

A cross-platform clipboard manipulation module for Python with support for multiple data formats.

## Features

- **Cross-Platform Support**: Works on Windows (Win32), MacOS (Cocoa), and Linux (XClip)
- **Multiple Formats**: Supports plain text, HTML, RTF, and images
- **Modular Design**: Easy to extend with custom backends
- **Type Hints**: Full type annotation support
- **No Required Dependencies**: Core functionality works without external packages

## Installation

```bash
pip install xclipboard
```

### Platform-Specific Dependencies

**MacOS:**
```bash
pip install xclipboard[macos]
# or
pip install pyobjc-framework-Cocoa
```

**Linux:**
```bash
# Install xclip system package
sudo apt-get install xclip  # Debian/Ubuntu
sudo dnf install xclip      # Fedora
sudo pacman -S xclip        # Arch Linux
```

**For Image Support (all platforms):**
```bash
pip install xclipboard[image]
# or
pip install Pillow
```

## Quick Start

```python
from xclipboard import Clipboard

clipboard = Clipboard()

# Set and get plain text
clipboard.set_text("Hello, World!")
text = clipboard.get_text()
print(text)  # Output: Hello, World!

# Set HTML with plain text fallback
clipboard.set_html("<b>Bold</b>", plain_text_fallback="Bold")

# Check available formats
formats = clipboard.get_available_formats()
print([f.name for f in formats])

# Clear clipboard
clipboard.clear()
```

## Usage Examples

### Plain Text

```python
from xclipboard import Clipboard

clipboard = Clipboard()

# Set text
clipboard.set_text("Hello, XClipboard!")

# Get text
text = clipboard.get_text()
```

### HTML Content

```python
from xclipboard import Clipboard

clipboard = Clipboard()

# Set HTML with fallback
html = "<h1>Title</h1><p>Paragraph with <strong>bold</strong> text.</p>"
clipboard.set_html(html, plain_text_fallback="Title\nParagraph with bold text.")

# Get HTML
html_content = clipboard.get_html()
```

### Rich Text Format (RTF)

```python
from xclipboard import Clipboard

clipboard = Clipboard()

rtf = r"{\rtf1\ansi This is \b bold\b0 text.}"
clipboard.set_rtf(rtf, plain_text_fallback="This is bold text.")

rtf_content = clipboard.get_rtf()
```

### Images

```python
from xclipboard import Clipboard

clipboard = Clipboard()

# Set image from PNG bytes
with open("image.png", "rb") as f:
    clipboard.set_image(f.read())

# Get image as PNG bytes
image_data = clipboard.get_image()
if image_data:
    with open("output.png", "wb") as f:
        f.write(image_data)
```

### Using ClipboardData

```python
from xclipboard import Clipboard, ClipboardFormat
from xclipboard.data_types import ClipboardData

clipboard = Clipboard()

# Create and set data
data = ClipboardData("Hello!", ClipboardFormat.PLAIN_TEXT)
clipboard.set(data)

# Get with automatic format detection
retrieved = clipboard.get()
print(retrieved.format_type.name)  # PLAIN_TEXT
print(retrieved.data)              # Hello!
```

### Check Clipboard State

```python
from xclipboard import Clipboard, ClipboardFormat

clipboard = Clipboard()

# Check if empty
if clipboard.is_empty():
    print("Clipboard is empty")

# Check for specific format
if clipboard.has_format(ClipboardFormat.IMAGE):
    image = clipboard.get_image()
```

### Custom Backend

```python
from xclipboard import Clipboard
from xclipboard.backends.base import ClipboardBackend

class MyCustomBackend(ClipboardBackend):
    # Implement abstract methods...
    pass

clipboard = Clipboard(backend=MyCustomBackend())
```

## API Reference

### Clipboard Class

| Method | Description |
|--------|-------------|
| `clear()` | Clear all clipboard contents |
| `get(format_type=None)` | Get clipboard content as ClipboardData |
| `get_available_formats()` | List available formats on clipboard |
| `get_html()` | Get HTML content |
| `get_image()` | Get image as PNG bytes |
| `get_rtf()` | Get RTF content |
| `get_text()` | Get plain text |
| `has_format(format_type)` | Check if format is available |
| `is_empty()` | Check if clipboard is empty |
| `set(data, plain_text_fallback=None)` | Set from ClipboardData |
| `set_html(html, plain_text_fallback=None)` | Set HTML content |
| `set_image(image_data)` | Set image (PNG bytes) |
| `set_rtf(rtf, plain_text_fallback=None)` | Set RTF content |
| `set_text(text)` | Set plain text |

### ClipboardFormat Enum

- `PLAIN_TEXT` - Plain text format
- `HTML` - HTML format
- `RTF` - Rich Text Format
- `IMAGE` - Image format (PNG)

## Exceptions

- `ClipboardError` - Base exception
- `ClipboardAccessError` - Cannot access clipboard
- `ClipboardFormatError` - Unsupported format
- `ClipboardPlatformError` - Unsupported platform
- `ClipboardTimeoutError` - Operation timed out

## License

MIT License
