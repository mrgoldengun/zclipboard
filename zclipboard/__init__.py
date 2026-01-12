"""
zclipboard - Cross-platform clipboard manipulation module.

Supports Windows (Win32), MacOS (Cocoa), and Linux (XClip).
Handles multiple clipboard representations: plain text, rich text, image, etc.
"""

from zclipboard.clipboard import Clipboard
from zclipboard.data_types import ClipboardFormat

__version__ = "1.0.1"
__all__ = ["Clipboard", "ClipboardFormat"]
