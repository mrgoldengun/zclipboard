"""
XClipboard - Cross-platform clipboard manipulation module.

Supports Windows (Win32), MacOS (Cocoa), and Linux (XClip).
Handles multiple clipboard representations: plain text, rich text, image, etc.
"""

from xclipboard.clipboard import Clipboard
from xclipboard.data_types import ClipboardFormat

__version__ = "1.0.0"
__all__ = ["Clipboard", "ClipboardFormat"]
