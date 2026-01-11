# Examples

This directory contains examples demonstrating how to use the XClipboard module.

## Available Examples

### basic_text.py
Basic plain text clipboard operations including set, get, and clear.

```bash
python examples/basic_text.py
```

### html_clipboard.py
Working with HTML content and plain text fallbacks.

```bash
python examples/html_clipboard.py
```

### rtf_clipboard.py
Rich Text Format (RTF) clipboard operations.

```bash
python examples/rtf_clipboard.py
```

### image_clipboard.py
Image clipboard operations (requires Pillow for test image generation).

```bash
pip install Pillow
python examples/image_clipboard.py
```

### clipboard_data_usage.py
Using the ClipboardData class for flexible clipboard operations.

```bash
python examples/clipboard_data_usage.py
```

### custom_backend.py
Creating and using a custom clipboard backend.

```bash
python examples/custom_backend.py
```

### clipboard_monitor.py
Monitor clipboard for changes in real-time.

```bash
python examples/clipboard_monitor.py
```

## Running Examples

1. Install the package:
```bash
pip install -e .
```

2. Run any example:
```bash
python examples/<example_name>.py
```
