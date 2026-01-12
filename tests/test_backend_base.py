"""Tests for base ClipboardBackend class."""

import pytest

from xclipboard.backends.base import ClipboardBackend


class TestClipboardBackendInterface:
    """Tests for ClipboardBackend abstract interface."""
    
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            ClipboardBackend()
    
    def test_required_methods_defined(self):
        required_methods = [
            "clear",
            "get_available_formats",
            "get_html",
            "get_image",
            "get_rtf",
            "get_text",
            "set_html",
            "set_image",
            "set_rtf",
            "set_text",
        ]
        
        for method_name in required_methods:
            assert hasattr(ClipboardBackend, method_name)
            method = getattr(ClipboardBackend, method_name)
            assert callable(method)
    
    def test_incomplete_implementation_raises_error(self):
        class IncompleteBackend(ClipboardBackend):
            def clear(self):
                pass
        
        with pytest.raises(TypeError):
            IncompleteBackend()


class TestMockBackendImplementation:
    """Tests verifying mock backend properly implements interface."""
    
    def test_mock_backend_instantiates(self, mock_backend):
        assert mock_backend is not None
    
    def test_mock_backend_is_clipboard_backend(self, mock_backend):
        assert isinstance(mock_backend, ClipboardBackend)
    
    def test_mock_backend_clear(self, mock_backend):
        mock_backend.set_text("test")
        mock_backend.clear()
        assert mock_backend.get_text() is None
    
    def test_mock_backend_text_operations(self, mock_backend):
        mock_backend.set_text("hello")
        assert mock_backend.get_text() == "hello"
    
    def test_mock_backend_html_operations(self, mock_backend, sample_html):
        mock_backend.set_html(sample_html, "fallback")
        assert mock_backend.get_html() == sample_html
        assert mock_backend.get_text() == "fallback"
    
    def test_mock_backend_rtf_operations(self, mock_backend, sample_rtf):
        mock_backend.set_rtf(sample_rtf, "fallback")
        assert mock_backend.get_rtf() == sample_rtf
        assert mock_backend.get_text() == "fallback"
    
    def test_mock_backend_image_operations(self, mock_backend, sample_png_bytes):
        mock_backend.set_image(sample_png_bytes)
        assert mock_backend.get_image() == sample_png_bytes
