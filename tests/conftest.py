"""Pytest configuration and shared fixtures."""

import sys
from typing import List, Optional
from unittest.mock import MagicMock

import pytest

from xclipboard import ClipboardFormat
from xclipboard.backends.base import ClipboardBackend


class MockClipboardBackend(ClipboardBackend):
    """Mock backend for testing without platform dependencies."""
    
    def __init__(self):
        self._storage = {}
    
    def clear(self) -> None:
        self._storage.clear()
    
    def get_available_formats(self) -> List[ClipboardFormat]:
        return list(self._storage.keys())
    
    def get_html(self) -> Optional[str]:
        return self._storage.get(ClipboardFormat.HTML)
    
    def get_image(self) -> Optional[bytes]:
        return self._storage.get(ClipboardFormat.IMAGE)
    
    def get_rtf(self) -> Optional[str]:
        return self._storage.get(ClipboardFormat.RTF)
    
    def get_text(self) -> Optional[str]:
        return self._storage.get(ClipboardFormat.PLAIN_TEXT)
    
    def set_html(self, html_content: str, plain_text_fallback: Optional[str] = None) -> None:
        self._storage.clear()
        self._storage[ClipboardFormat.HTML] = html_content
        if plain_text_fallback:
            self._storage[ClipboardFormat.PLAIN_TEXT] = plain_text_fallback
    
    def set_image(self, image_data: bytes) -> None:
        self._storage.clear()
        self._storage[ClipboardFormat.IMAGE] = image_data
    
    def set_rtf(self, rtf_content: str, plain_text_fallback: Optional[str] = None) -> None:
        self._storage.clear()
        self._storage[ClipboardFormat.RTF] = rtf_content
        if plain_text_fallback:
            self._storage[ClipboardFormat.PLAIN_TEXT] = plain_text_fallback
    
    def set_text(self, text: str) -> None:
        self._storage.clear()
        self._storage[ClipboardFormat.PLAIN_TEXT] = text


@pytest.fixture
def mock_backend():
    """Provide a mock clipboard backend."""
    return MockClipboardBackend()


@pytest.fixture
def clipboard_with_mock(mock_backend):
    """Provide a Clipboard instance with mock backend."""
    from xclipboard import Clipboard
    return Clipboard(backend=mock_backend)


@pytest.fixture
def sample_html():
    """Provide sample HTML content."""
    return "<h1>Test</h1><p>This is <strong>bold</strong> text.</p>"


@pytest.fixture
def sample_rtf():
    """Provide sample RTF content."""
    return r"{\rtf1\ansi\deff0 This is \b bold\b0 text.}"


@pytest.fixture
def sample_png_bytes():
    """Provide minimal valid PNG bytes."""
    # Minimal 1x1 transparent PNG
    return (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01'
        b'\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )


def is_platform(name: str) -> bool:
    """Check if running on specific platform."""
    platform_map = {
        "darwin": sys.platform == "darwin",
        "linux": sys.platform.startswith("linux"),
        "windows": sys.platform == "win32",
    }
    return platform_map.get(name, False)


def skip_unless_platform(platform: str):
    """Decorator to skip tests unless on specific platform."""
    return pytest.mark.skipif(
        not is_platform(platform),
        reason=f"Test requires {platform} platform"
    )


skip_unless_windows = skip_unless_platform("windows")
skip_unless_macos = skip_unless_platform("darwin")
skip_unless_linux = skip_unless_platform("linux")
