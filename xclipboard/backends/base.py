"""Abstract base class for clipboard backends."""

from abc import ABC, abstractmethod
from typing import List, Optional

from xclipboard.data_types import ClipboardFormat


class ClipboardBackend(ABC):
    """Abstract base class defining the clipboard backend interface."""
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all clipboard contents."""
        pass
    
    @abstractmethod
    def get_available_formats(self) -> List[ClipboardFormat]:
        """Return list of available formats currently on clipboard."""
        pass
    
    @abstractmethod
    def get_html(self) -> Optional[str]:
        """Get HTML content from clipboard."""
        pass
    
    @abstractmethod
    def get_image(self) -> Optional[bytes]:
        """Get image data from clipboard as PNG bytes."""
        pass
    
    @abstractmethod
    def get_rtf(self) -> Optional[str]:
        """Get RTF content from clipboard."""
        pass
    
    @abstractmethod
    def get_text(self) -> Optional[str]:
        """Get plain text from clipboard."""
        pass
    
    @abstractmethod
    def set_html(self, html_content: str, plain_text_fallback: Optional[str] = None) -> None:
        """Set HTML content to clipboard with optional plain text fallback."""
        pass
    
    @abstractmethod
    def set_image(self, image_data: bytes) -> None:
        """Set image data to clipboard (expects PNG format)."""
        pass
    
    @abstractmethod
    def set_rtf(self, rtf_content: str, plain_text_fallback: Optional[str] = None) -> None:
        """Set RTF content to clipboard with optional plain text fallback."""
        pass
    
    @abstractmethod
    def set_text(self, text: str) -> None:
        """Set plain text to clipboard."""
        pass
