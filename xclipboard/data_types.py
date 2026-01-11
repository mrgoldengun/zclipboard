"""Clipboard data types and format definitions."""

from enum import Enum, auto
from typing import Any, Optional


class ClipboardFormat(Enum):
    """Supported clipboard data formats."""
    
    HTML = auto()
    IMAGE = auto()
    PLAIN_TEXT = auto()
    RTF = auto()
    
    @classmethod
    def from_string(cls, format_string: str) -> Optional["ClipboardFormat"]:
        """Convert string representation to ClipboardFormat enum."""
        format_map = {
            "html": cls.HTML,
            "image": cls.IMAGE,
            "plain_text": cls.PLAIN_TEXT,
            "rtf": cls.RTF,
            "text": cls.PLAIN_TEXT,
        }
        return format_map.get(format_string.lower())


class ClipboardData:
    """Container for clipboard data with format information."""
    
    def __init__(self, data: Any, format_type: ClipboardFormat):
        self.data = data
        self.format_type = format_type
    
    def __repr__(self) -> str:
        return f"ClipboardData(format={self.format_type.name}, data_type={type(self.data).__name__})"
