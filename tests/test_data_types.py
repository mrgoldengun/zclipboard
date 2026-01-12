"""Tests for data_types module."""

import pytest

from xclipboard.data_types import ClipboardData, ClipboardFormat


class TestClipboardFormat:
    """Tests for ClipboardFormat enum."""
    
    def test_format_values_exist(self):
        assert ClipboardFormat.HTML is not None
        assert ClipboardFormat.IMAGE is not None
        assert ClipboardFormat.PLAIN_TEXT is not None
        assert ClipboardFormat.RTF is not None
    
    def test_from_string_valid_formats(self):
        assert ClipboardFormat.from_string("html") == ClipboardFormat.HTML
        assert ClipboardFormat.from_string("HTML") == ClipboardFormat.HTML
        assert ClipboardFormat.from_string("image") == ClipboardFormat.IMAGE
        assert ClipboardFormat.from_string("plain_text") == ClipboardFormat.PLAIN_TEXT
        assert ClipboardFormat.from_string("text") == ClipboardFormat.PLAIN_TEXT
        assert ClipboardFormat.from_string("rtf") == ClipboardFormat.RTF
    
    def test_from_string_invalid_format(self):
        assert ClipboardFormat.from_string("invalid") is None
        assert ClipboardFormat.from_string("") is None
        assert ClipboardFormat.from_string("unknown_format") is None


class TestClipboardData:
    """Tests for ClipboardData class."""
    
    def test_create_with_text(self):
        data = ClipboardData("test text", ClipboardFormat.PLAIN_TEXT)
        assert data.data == "test text"
        assert data.format_type == ClipboardFormat.PLAIN_TEXT
    
    def test_create_with_html(self):
        html = "<p>test</p>"
        data = ClipboardData(html, ClipboardFormat.HTML)
        assert data.data == html
        assert data.format_type == ClipboardFormat.HTML
    
    def test_create_with_image_bytes(self):
        image_bytes = b"\x89PNG\r\n\x1a\n"
        data = ClipboardData(image_bytes, ClipboardFormat.IMAGE)
        assert data.data == image_bytes
        assert data.format_type == ClipboardFormat.IMAGE
    
    def test_repr_contains_format_and_type(self):
        data = ClipboardData("test", ClipboardFormat.PLAIN_TEXT)
        repr_str = repr(data)
        assert "PLAIN_TEXT" in repr_str
        assert "str" in repr_str
    
    def test_repr_with_bytes(self):
        data = ClipboardData(b"bytes", ClipboardFormat.IMAGE)
        repr_str = repr(data)
        assert "IMAGE" in repr_str
        assert "bytes" in repr_str
