"""Tests for MacOS clipboard backend."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import skip_unless_macos


class TestMacOSBackendImport:
    """Tests for MacOS backend import behavior."""
    
    @skip_unless_macos
    def test_import_on_macos_with_pyobjc(self):
        try:
            from xclipboard.backends.macos import MacOSClipboardBackend
            assert MacOSClipboardBackend is not None
        except Exception as e:
            # PyObjC might not be installed
            assert "pyobjc" in str(e).lower() or "PyObjC" in str(e)


class TestMacOSBackendWithMock:
    """Tests for MacOS backend with mocked PyObjC."""
    
    def test_backend_requires_pyobjc(self):
        # Mock PyObjC not available
        with patch.dict(sys.modules, {"objc": None, "AppKit": None}):
            # Force reimport
            import importlib
            
            # This should handle the ImportError gracefully
            try:
                from xclipboard.backends import macos
                importlib.reload(macos)
            except ImportError:
                pass


@skip_unless_macos
class TestMacOSBackendIntegration:
    """Integration tests for MacOS backend (requires MacOS with PyObjC)."""
    
    @pytest.fixture
    def macos_backend(self):
        try:
            from xclipboard.backends.macos import MacOSClipboardBackend
            return MacOSClipboardBackend()
        except Exception:
            pytest.skip("PyObjC not available")
    
    def test_instantiation(self, macos_backend):
        assert macos_backend is not None
    
    def test_set_and_get_text(self, macos_backend):
        test_text = "MacOS clipboard test"
        
        macos_backend.set_text(test_text)
        result = macos_backend.get_text()
        
        assert result == test_text
    
    def test_clear_clipboard(self, macos_backend):
        macos_backend.set_text("test")
        macos_backend.clear()
        
        formats = macos_backend.get_available_formats()
        assert len(formats) == 0 or macos_backend.get_text() is None
    
    def test_get_available_formats(self, macos_backend):
        macos_backend.set_text("test")
        
        formats = macos_backend.get_available_formats()
        assert isinstance(formats, list)
    
    def test_set_html_with_fallback(self, macos_backend):
        html = "<b>test</b>"
        fallback = "test"
        
        macos_backend.set_html(html, fallback)
        
        # Should have both HTML and text available
        result_text = macos_backend.get_text()
        assert result_text == fallback
    
    def test_unicode_text(self, macos_backend):
        unicode_text = "Hello 世界 🌍"
        
        macos_backend.set_text(unicode_text)
        result = macos_backend.get_text()
        
        assert result == unicode_text
