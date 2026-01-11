"""Main clipboard interface - platform-agnostic API."""

import sys
from typing import List, Optional, Type

from xclipboard.backends.base import ClipboardBackend
from xclipboard.data_types import ClipboardData, ClipboardFormat
from xclipboard.exceptions import ClipboardFormatError, ClipboardPlatformError


def _get_platform_backend() -> Type[ClipboardBackend]:
    """Get the appropriate backend class for the current platform."""
    platform = sys.platform
    
    if platform == "win32":
        from xclipboard.backends.windows import WindowsClipboardBackend
        return WindowsClipboardBackend
    elif platform == "darwin":
        from xclipboard.backends.macos import MacOSClipboardBackend
        return MacOSClipboardBackend
    elif platform.startswith("linux"):
        from xclipboard.backends.linux import LinuxClipboardBackend
        return LinuxClipboardBackend
    else:
        raise ClipboardPlatformError(f"Unsupported platform: {platform}")


class Clipboard:
    """Cross-platform clipboard interface."""
    
    def __init__(self, backend: Optional[ClipboardBackend] = None):
        """
        Initialize clipboard with optional custom backend.
        
        Args:
            backend: Custom backend instance. If None, auto-detects platform.
        """
        if backend is not None:
            self._backend = backend
        else:
            backend_class = _get_platform_backend()
            self._backend = backend_class()
    
    @property
    def backend(self) -> ClipboardBackend:
        """Get the current clipboard backend."""
        return self._backend
    
    def clear(self) -> None:
        """Clear all clipboard contents."""
        self._backend.clear()
    
    def get(self, format_type: Optional[ClipboardFormat] = None) -> Optional[ClipboardData]:
        """
        Get clipboard content in the specified format.
        
        Args:
            format_type: Desired format. If None, returns first available format.
            
        Returns:
            ClipboardData object or None if clipboard is empty.
        """
        if format_type is None:
            available = self.get_available_formats()
            if not available:
                return None
            format_type = available[0]
        
        data = None
        if format_type == ClipboardFormat.PLAIN_TEXT:
            data = self._backend.get_text()
        elif format_type == ClipboardFormat.HTML:
            data = self._backend.get_html()
        elif format_type == ClipboardFormat.RTF:
            data = self._backend.get_rtf()
        elif format_type == ClipboardFormat.IMAGE:
            data = self._backend.get_image()
        else:
            raise ClipboardFormatError(f"Unsupported format: {format_type}")
        
        if data is not None:
            return ClipboardData(data, format_type)
        return None
    
    def get_available_formats(self) -> List[ClipboardFormat]:
        """Get list of available formats currently on clipboard."""
        return self._backend.get_available_formats()
    
    def get_html(self) -> Optional[str]:
        """Get HTML content from clipboard."""
        return self._backend.get_html()
    
    def get_image(self) -> Optional[bytes]:
        """Get image data from clipboard as PNG bytes."""
        return self._backend.get_image()
    
    def get_rtf(self) -> Optional[str]:
        """Get RTF content from clipboard."""
        return self._backend.get_rtf()
    
    def get_text(self) -> Optional[str]:
        """Get plain text from clipboard."""
        return self._backend.get_text()
    
    def has_format(self, format_type: ClipboardFormat) -> bool:
        """Check if clipboard contains data in the specified format."""
        return format_type in self.get_available_formats()
    
    def is_empty(self) -> bool:
        """Check if clipboard is empty."""
        return len(self.get_available_formats()) == 0
    
    def set(self, data: ClipboardData, plain_text_fallback: Optional[str] = None) -> None:
        """
        Set clipboard content from ClipboardData object.
        
        Args:
            data: ClipboardData object containing the data and format.
            plain_text_fallback: Optional plain text fallback for rich formats.
        """
        if data.format_type == ClipboardFormat.PLAIN_TEXT:
            self._backend.set_text(data.data)
        elif data.format_type == ClipboardFormat.HTML:
            self._backend.set_html(data.data, plain_text_fallback)
        elif data.format_type == ClipboardFormat.RTF:
            self._backend.set_rtf(data.data, plain_text_fallback)
        elif data.format_type == ClipboardFormat.IMAGE:
            self._backend.set_image(data.data)
        else:
            raise ClipboardFormatError(f"Unsupported format: {data.format_type}")
    
    def set_html(self, html_content: str, plain_text_fallback: Optional[str] = None) -> None:
        """
        Set HTML content to clipboard.
        
        Args:
            html_content: HTML content to set.
            plain_text_fallback: Optional plain text fallback.
        """
        self._backend.set_html(html_content, plain_text_fallback)
    
    def set_image(self, image_data: bytes) -> None:
        """
        Set image data to clipboard.
        
        Args:
            image_data: PNG image data as bytes.
        """
        self._backend.set_image(image_data)
    
    def set_rtf(self, rtf_content: str, plain_text_fallback: Optional[str] = None) -> None:
        """
        Set RTF content to clipboard.
        
        Args:
            rtf_content: RTF content to set.
            plain_text_fallback: Optional plain text fallback.
        """
        self._backend.set_rtf(rtf_content, plain_text_fallback)
    
    def set_text(self, text: str) -> None:
        """
        Set plain text to clipboard.
        
        Args:
            text: Text to set.
        """
        self._backend.set_text(text)
