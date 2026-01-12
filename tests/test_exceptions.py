"""Tests for exceptions module."""

import pytest

from xclipboard.exceptions import (
    ClipboardAccessError,
    ClipboardError,
    ClipboardFormatError,
    ClipboardPlatformError,
    ClipboardTimeoutError,
)


class TestExceptions:
    """Tests for custom exception classes."""
    
    def test_clipboard_error_is_base_exception(self):
        assert issubclass(ClipboardError, Exception)
    
    def test_clipboard_access_error_inherits_from_base(self):
        assert issubclass(ClipboardAccessError, ClipboardError)
        
        with pytest.raises(ClipboardError):
            raise ClipboardAccessError("test")
    
    def test_clipboard_format_error_inherits_from_base(self):
        assert issubclass(ClipboardFormatError, ClipboardError)
        
        with pytest.raises(ClipboardError):
            raise ClipboardFormatError("test")
    
    def test_clipboard_platform_error_inherits_from_base(self):
        assert issubclass(ClipboardPlatformError, ClipboardError)
        
        with pytest.raises(ClipboardError):
            raise ClipboardPlatformError("test")
    
    def test_clipboard_timeout_error_inherits_from_base(self):
        assert issubclass(ClipboardTimeoutError, ClipboardError)
        
        with pytest.raises(ClipboardError):
            raise ClipboardTimeoutError("test")
    
    def test_exception_message_preserved(self):
        message = "Custom error message"
        
        error = ClipboardAccessError(message)
        assert str(error) == message
        
        error = ClipboardFormatError(message)
        assert str(error) == message
        
        error = ClipboardPlatformError(message)
        assert str(error) == message
        
        error = ClipboardTimeoutError(message)
        assert str(error) == message
