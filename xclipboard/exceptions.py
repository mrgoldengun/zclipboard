"""Custom exceptions for XClipboard module."""


class ClipboardError(Exception):
    """Base exception for clipboard operations."""
    pass


class ClipboardAccessError(ClipboardError):
    """Raised when clipboard cannot be accessed."""
    pass


class ClipboardFormatError(ClipboardError):
    """Raised when clipboard format is not supported or invalid."""
    pass


class ClipboardPlatformError(ClipboardError):
    """Raised when platform is not supported."""
    pass


class ClipboardTimeoutError(ClipboardError):
    """Raised when clipboard operation times out."""
    pass
