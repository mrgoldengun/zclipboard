"""Cross-platform integration tests.

These tests run on the current platform using the actual clipboard.
They verify end-to-end functionality.
"""

import sys

import pytest

from xclipboard import Clipboard, ClipboardFormat
from xclipboard.data_types import ClipboardData


def get_native_clipboard():
    """Get clipboard with native backend, or skip if not available."""
    try:
        return Clipboard()
    except Exception as e:
        pytest.skip(f"Native clipboard not available: {e}")


@pytest.mark.integration
class TestNativeClipboardText:
    """Integration tests for text operations on native clipboard."""
    
    @pytest.fixture
    def clipboard(self):
        return get_native_clipboard()
    
    def test_set_and_get_simple_text(self, clipboard):
        test_text = "Integration test text"
        
        clipboard.set_text(test_text)
        result = clipboard.get_text()
        
        assert result == test_text
    
    def test_set_and_get_unicode_text(self, clipboard):
        test_text = "Unicode: 日本語 中文 한국어 🎉"
        
        clipboard.set_text(test_text)
        result = clipboard.get_text()
        
        assert result == test_text
    
    def test_set_and_get_multiline_text(self, clipboard):
        test_text = "Line 1\nLine 2\nLine 3"
        
        clipboard.set_text(test_text)
        result = clipboard.get_text()
        
        assert result == test_text
    
    def test_set_and_get_empty_text(self, clipboard):
        clipboard.set_text("")
        result = clipboard.get_text()
        
        # Behavior may vary by platform
        assert result == "" or result is None
    
    def test_text_overwrites_previous(self, clipboard):
        clipboard.set_text("First")
        clipboard.set_text("Second")
        
        assert clipboard.get_text() == "Second"


@pytest.mark.integration
class TestNativeClipboardFormats:
    """Integration tests for format detection."""
    
    @pytest.fixture
    def clipboard(self):
        return get_native_clipboard()
    
    def test_text_format_available_after_set(self, clipboard):
        clipboard.set_text("test")
        
        formats = clipboard.get_available_formats()
        
        assert ClipboardFormat.PLAIN_TEXT in formats
    
    def test_has_format_returns_true(self, clipboard):
        clipboard.set_text("test")
        
        assert clipboard.has_format(ClipboardFormat.PLAIN_TEXT)
    
    def test_is_empty_after_clear(self, clipboard):
        clipboard.set_text("test")
        clipboard.clear()
        
        # Give clipboard time to process
        import time
        time.sleep(0.1)
        
        # Some platforms may not fully clear
        formats = clipboard.get_available_formats()
        text = clipboard.get_text()
        
        assert len(formats) == 0 or text is None or text == ""


@pytest.mark.integration
class TestNativeClipboardData:
    """Integration tests for ClipboardData operations."""
    
    @pytest.fixture
    def clipboard(self):
        return get_native_clipboard()
    
    def test_set_and_get_via_clipboard_data(self, clipboard):
        data = ClipboardData("ClipboardData test", ClipboardFormat.PLAIN_TEXT)
        
        clipboard.set(data)
        result = clipboard.get(ClipboardFormat.PLAIN_TEXT)
        
        assert result is not None
        assert result.data == "ClipboardData test"
        assert result.format_type == ClipboardFormat.PLAIN_TEXT
    
    def test_get_with_auto_format(self, clipboard):
        clipboard.set_text("Auto format test")
        
        result = clipboard.get()
        
        assert result is not None
        assert "Auto format test" in result.data


@pytest.mark.integration
@pytest.mark.slow
class TestNativeClipboardHtml:
    """Integration tests for HTML operations (may not work on all platforms)."""
    
    @pytest.fixture
    def clipboard(self):
        return get_native_clipboard()
    
    def test_set_html_with_fallback(self, clipboard):
        html = "<b>Bold</b>"
        fallback = "Bold"
        
        clipboard.set_html(html, plain_text_fallback=fallback)
        
        # At minimum, plain text should be available
        text = clipboard.get_text()
        assert text is not None
    
    def test_html_format_detection(self, clipboard):
        html = "<p>Test</p>"
        
        clipboard.set_html(html, plain_text_fallback="Test")
        
        formats = clipboard.get_available_formats()
        
        # HTML format availability varies by platform
        has_html = ClipboardFormat.HTML in formats
        has_text = ClipboardFormat.PLAIN_TEXT in formats
        
        assert has_html or has_text
