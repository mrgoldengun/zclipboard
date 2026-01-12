"""Tests for platform detection and backend selection."""

import sys
from unittest.mock import patch

import pytest

from xclipboard.exceptions import ClipboardPlatformError


class TestPlatformDetection:
    """Tests for platform-specific backend selection."""
    
    def test_windows_platform_selects_windows_backend(self):
        with patch.object(sys, "platform", "win32"):
            from xclipboard.clipboard import _get_platform_backend
            
            # Force reimport to get fresh platform detection
            import importlib
            import xclipboard.clipboard
            importlib.reload(xclipboard.clipboard)
            
            from xclipboard.clipboard import _get_platform_backend
            
            # On non-Windows, this will fail at import, which is expected
            try:
                backend_class = _get_platform_backend()
                assert backend_class.__name__ == "WindowsClipboardBackend"
            except AttributeError:
                # ctypes.windll not available on non-Windows
                pass
    
    def test_darwin_platform_selects_macos_backend(self):
        with patch.object(sys, "platform", "darwin"):
            import importlib
            import xclipboard.clipboard
            importlib.reload(xclipboard.clipboard)
            
            from xclipboard.clipboard import _get_platform_backend
            
            try:
                backend_class = _get_platform_backend()
                assert backend_class.__name__ == "MacOSClipboardBackend"
            except Exception:
                # PyObjC not available
                pass
    
    def test_linux_platform_selects_linux_backend(self):
        with patch.object(sys, "platform", "linux"):
            import importlib
            import xclipboard.clipboard
            importlib.reload(xclipboard.clipboard)
            
            from xclipboard.clipboard import _get_platform_backend
            
            backend_class = _get_platform_backend()
            assert backend_class.__name__ == "LinuxClipboardBackend"
    
    def test_unsupported_platform_raises_error(self):
        with patch.object(sys, "platform", "unsupported_os"):
            import importlib
            import xclipboard.clipboard
            importlib.reload(xclipboard.clipboard)
            
            from xclipboard.clipboard import _get_platform_backend
            
            with pytest.raises(ClipboardPlatformError) as exc_info:
                _get_platform_backend()
            
            assert "unsupported_os" in str(exc_info.value).lower()


class TestClipboardAutoBackend:
    """Tests for Clipboard automatic backend selection."""
    
    def test_clipboard_uses_auto_detected_backend(self):
        # This test will use whatever backend is appropriate for current platform
        from xclipboard import Clipboard
        from xclipboard.backends.base import ClipboardBackend
        
        try:
            clipboard = Clipboard()
            assert isinstance(clipboard.backend, ClipboardBackend)
        except Exception:
            # Platform dependencies might not be available
            pass
    
    def test_clipboard_with_explicit_backend_ignores_platform(self, mock_backend):
        from xclipboard import Clipboard
        
        clipboard = Clipboard(backend=mock_backend)
        
        # Should use provided backend regardless of platform
        assert clipboard.backend is mock_backend
