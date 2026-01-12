"""Tests for main Clipboard class."""

import pytest

from xclipboard import Clipboard, ClipboardFormat
from xclipboard.data_types import ClipboardData
from xclipboard.exceptions import ClipboardFormatError


class TestClipboardInitialization:
    """Tests for Clipboard initialization."""
    
    def test_init_with_custom_backend(self, mock_backend):
        clipboard = Clipboard(backend=mock_backend)
        assert clipboard.backend is mock_backend
    
    def test_backend_property_returns_backend(self, clipboard_with_mock, mock_backend):
        assert clipboard_with_mock.backend is mock_backend


class TestClipboardTextOperations:
    """Tests for plain text clipboard operations."""
    
    def test_set_and_get_text(self, clipboard_with_mock):
        clipboard_with_mock.set_text("Hello, World!")
        assert clipboard_with_mock.get_text() == "Hello, World!"
    
    def test_set_text_clears_previous_content(self, clipboard_with_mock):
        clipboard_with_mock.set_text("First")
        clipboard_with_mock.set_text("Second")
        assert clipboard_with_mock.get_text() == "Second"
    
    def test_get_text_returns_none_when_empty(self, clipboard_with_mock):
        clipboard_with_mock.clear()
        assert clipboard_with_mock.get_text() is None
    
    def test_set_text_with_unicode(self, clipboard_with_mock):
        unicode_text = "Hello 世界 🌍 مرحبا"
        clipboard_with_mock.set_text(unicode_text)
        assert clipboard_with_mock.get_text() == unicode_text
    
    def test_set_text_with_multiline(self, clipboard_with_mock):
        multiline = "Line 1\nLine 2\nLine 3"
        clipboard_with_mock.set_text(multiline)
        assert clipboard_with_mock.get_text() == multiline


class TestClipboardHtmlOperations:
    """Tests for HTML clipboard operations."""
    
    def test_set_and_get_html(self, clipboard_with_mock, sample_html):
        clipboard_with_mock.set_html(sample_html)
        assert clipboard_with_mock.get_html() == sample_html
    
    def test_set_html_with_fallback(self, clipboard_with_mock, sample_html):
        fallback = "Test - This is bold text."
        clipboard_with_mock.set_html(sample_html, plain_text_fallback=fallback)
        assert clipboard_with_mock.get_html() == sample_html
        assert clipboard_with_mock.get_text() == fallback
    
    def test_get_html_returns_none_when_empty(self, clipboard_with_mock):
        clipboard_with_mock.clear()
        assert clipboard_with_mock.get_html() is None


class TestClipboardRtfOperations:
    """Tests for RTF clipboard operations."""
    
    def test_set_and_get_rtf(self, clipboard_with_mock, sample_rtf):
        clipboard_with_mock.set_rtf(sample_rtf)
        assert clipboard_with_mock.get_rtf() == sample_rtf
    
    def test_set_rtf_with_fallback(self, clipboard_with_mock, sample_rtf):
        fallback = "This is bold text."
        clipboard_with_mock.set_rtf(sample_rtf, plain_text_fallback=fallback)
        assert clipboard_with_mock.get_rtf() == sample_rtf
        assert clipboard_with_mock.get_text() == fallback
    
    def test_get_rtf_returns_none_when_empty(self, clipboard_with_mock):
        clipboard_with_mock.clear()
        assert clipboard_with_mock.get_rtf() is None


class TestClipboardImageOperations:
    """Tests for image clipboard operations."""
    
    def test_set_and_get_image(self, clipboard_with_mock, sample_png_bytes):
        clipboard_with_mock.set_image(sample_png_bytes)
        assert clipboard_with_mock.get_image() == sample_png_bytes
    
    def test_get_image_returns_none_when_empty(self, clipboard_with_mock):
        clipboard_with_mock.clear()
        assert clipboard_with_mock.get_image() is None


class TestClipboardClear:
    """Tests for clipboard clear operation."""
    
    def test_clear_removes_text(self, clipboard_with_mock):
        clipboard_with_mock.set_text("test")
        clipboard_with_mock.clear()
        assert clipboard_with_mock.get_text() is None
    
    def test_clear_removes_all_formats(self, clipboard_with_mock, sample_html):
        clipboard_with_mock.set_html(sample_html, "fallback")
        clipboard_with_mock.clear()
        assert clipboard_with_mock.get_html() is None
        assert clipboard_with_mock.get_text() is None


class TestClipboardFormats:
    """Tests for clipboard format detection."""
    
    def test_get_available_formats_empty(self, clipboard_with_mock):
        clipboard_with_mock.clear()
        assert clipboard_with_mock.get_available_formats() == []
    
    def test_get_available_formats_with_text(self, clipboard_with_mock):
        clipboard_with_mock.set_text("test")
        formats = clipboard_with_mock.get_available_formats()
        assert ClipboardFormat.PLAIN_TEXT in formats
    
    def test_get_available_formats_with_html_and_fallback(self, clipboard_with_mock, sample_html):
        clipboard_with_mock.set_html(sample_html, "fallback")
        formats = clipboard_with_mock.get_available_formats()
        assert ClipboardFormat.HTML in formats
        assert ClipboardFormat.PLAIN_TEXT in formats
    
    def test_has_format_true(self, clipboard_with_mock):
        clipboard_with_mock.set_text("test")
        assert clipboard_with_mock.has_format(ClipboardFormat.PLAIN_TEXT) is True
    
    def test_has_format_false(self, clipboard_with_mock):
        clipboard_with_mock.set_text("test")
        assert clipboard_with_mock.has_format(ClipboardFormat.IMAGE) is False
    
    def test_is_empty_true(self, clipboard_with_mock):
        clipboard_with_mock.clear()
        assert clipboard_with_mock.is_empty() is True
    
    def test_is_empty_false(self, clipboard_with_mock):
        clipboard_with_mock.set_text("test")
        assert clipboard_with_mock.is_empty() is False


class TestClipboardDataOperations:
    """Tests for ClipboardData-based operations."""
    
    def test_set_with_clipboard_data_text(self, clipboard_with_mock):
        data = ClipboardData("test", ClipboardFormat.PLAIN_TEXT)
        clipboard_with_mock.set(data)
        assert clipboard_with_mock.get_text() == "test"
    
    def test_set_with_clipboard_data_html(self, clipboard_with_mock, sample_html):
        data = ClipboardData(sample_html, ClipboardFormat.HTML)
        clipboard_with_mock.set(data, plain_text_fallback="fallback")
        assert clipboard_with_mock.get_html() == sample_html
        assert clipboard_with_mock.get_text() == "fallback"
    
    def test_set_with_clipboard_data_image(self, clipboard_with_mock, sample_png_bytes):
        data = ClipboardData(sample_png_bytes, ClipboardFormat.IMAGE)
        clipboard_with_mock.set(data)
        assert clipboard_with_mock.get_image() == sample_png_bytes
    
    def test_get_returns_clipboard_data(self, clipboard_with_mock):
        clipboard_with_mock.set_text("test")
        result = clipboard_with_mock.get(ClipboardFormat.PLAIN_TEXT)
        assert isinstance(result, ClipboardData)
        assert result.data == "test"
        assert result.format_type == ClipboardFormat.PLAIN_TEXT
    
    def test_get_returns_none_when_empty(self, clipboard_with_mock):
        clipboard_with_mock.clear()
        result = clipboard_with_mock.get(ClipboardFormat.PLAIN_TEXT)
        assert result is None
    
    def test_get_with_auto_format_detection(self, clipboard_with_mock):
        clipboard_with_mock.set_text("test")
        result = clipboard_with_mock.get()
        assert result is not None
        assert result.data == "test"
    
    def test_get_auto_returns_none_when_empty(self, clipboard_with_mock):
        clipboard_with_mock.clear()
        result = clipboard_with_mock.get()
        assert result is None
