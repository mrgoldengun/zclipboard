"""Tests for Windows clipboard backend."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import skip_unless_windows


class TestWindowsBackendImport:
    """Tests for Windows backend import behavior."""
    
    @skip_unless_windows
    def test_import_on_windows(self):
        from xclipboard.backends.windows import WindowsClipboardBackend
        assert WindowsClipboardBackend is not None
    
    @pytest.mark.skipif(sys.platform == "win32", reason="Test for non-Windows platforms")
    def test_import_fails_gracefully_on_non_windows(self):
        # On non-Windows, ctypes.windll doesn't exist
        with pytest.raises(AttributeError):
            from xclipboard.backends.windows import WindowsClipboardBackend


class TestWindowsBackendHtmlFormat:
    """Tests for Windows HTML clipboard format handling."""
    
    @skip_unless_windows
    def test_create_html_format(self):
        from xclipboard.backends.windows import WindowsClipboardBackend
        
        backend = WindowsClipboardBackend()
        html = "<b>test</b>"
        result = backend._create_html_format(html)
        
        assert "Version:0.9" in result
        assert "StartHTML:" in result
        assert "EndHTML:" in result
        assert "StartFragment:" in result
        assert "EndFragment:" in result
        assert "<!--StartFragment-->" in result
        assert "<!--EndFragment-->" in result
        assert html in result
    
    @skip_unless_windows
    def test_parse_html_format(self):
        from xclipboard.backends.windows import WindowsClipboardBackend
        
        backend = WindowsClipboardBackend()
        html_format = "Header<!--StartFragment--><b>test</b><!--EndFragment-->Footer"
        result = backend._parse_html_format(html_format)
        
        assert result == "<b>test</b>"
    
    @skip_unless_windows
    def test_parse_html_format_without_markers(self):
        from xclipboard.backends.windows import WindowsClipboardBackend
        
        backend = WindowsClipboardBackend()
        html = "<b>test</b>"
        result = backend._parse_html_format(html)
        
        assert result == html


@skip_unless_windows
class TestWindowsBackendIntegration:
    """Integration tests for Windows backend (requires Windows)."""
    
    def test_instantiation(self):
        from xclipboard.backends.windows import WindowsClipboardBackend
        
        backend = WindowsClipboardBackend()
        assert backend is not None
    
    def test_set_and_get_text(self):
        from xclipboard.backends.windows import WindowsClipboardBackend
        
        backend = WindowsClipboardBackend()
        test_text = "Windows clipboard test"
        
        backend.set_text(test_text)
        result = backend.get_text()
        
        assert result == test_text
    
    def test_clear_clipboard(self):
        from xclipboard.backends.windows import WindowsClipboardBackend
        
        backend = WindowsClipboardBackend()
        backend.set_text("test")
        backend.clear()
        
        result = backend.get_text()
        assert result is None or result == ""
    
    def test_get_available_formats(self):
        from xclipboard.backends.windows import WindowsClipboardBackend
        
        backend = WindowsClipboardBackend()
        backend.set_text("test")
        
        formats = backend.get_available_formats()
        assert isinstance(formats, list)
