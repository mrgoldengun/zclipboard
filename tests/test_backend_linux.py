"""Tests for Linux clipboard backend."""

import shutil
import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import skip_unless_linux
from xclipboard.exceptions import ClipboardAccessError, ClipboardTimeoutError


class TestLinuxBackendImport:
    """Tests for Linux backend import behavior."""
    
    def test_import_succeeds(self):
        from xclipboard.backends.linux import LinuxClipboardBackend
        assert LinuxClipboardBackend is not None


class TestLinuxBackendXclipDetection:
    """Tests for xclip detection."""
    
    def test_raises_error_when_xclip_not_found(self):
        with patch("shutil.which", return_value=None):
            from xclipboard.backends.linux import LinuxClipboardBackend
            
            with pytest.raises(ClipboardAccessError) as exc_info:
                LinuxClipboardBackend()
            
            assert "xclip" in str(exc_info.value)
    
    def test_initializes_when_xclip_found(self):
        with patch("shutil.which", return_value="/usr/bin/xclip"):
            from xclipboard.backends.linux import LinuxClipboardBackend
            
            backend = LinuxClipboardBackend()
            assert backend._xclip_path == "/usr/bin/xclip"


class TestLinuxBackendWithMock:
    """Tests for Linux backend with mocked subprocess."""
    
    @pytest.fixture
    def mock_xclip_backend(self):
        with patch("shutil.which", return_value="/usr/bin/xclip"):
            from xclipboard.backends.linux import LinuxClipboardBackend
            return LinuxClipboardBackend()
    
    def test_get_text_calls_xclip(self, mock_xclip_backend):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout=b"test text"
            )
            
            result = mock_xclip_backend.get_text()
            
            assert result == "test text"
            mock_run.assert_called()
    
    def test_get_text_returns_none_on_failure(self, mock_xclip_backend):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout=b""
            )
            
            result = mock_xclip_backend.get_text()
            
            assert result is None
    
    def test_set_text_calls_xclip(self, mock_xclip_backend):
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.returncode = 0
            mock_process.communicate.return_value = (b"", b"")
            mock_popen.return_value = mock_process
            
            mock_xclip_backend.set_text("test")
            
            mock_popen.assert_called()
            mock_process.communicate.assert_called()
    
    def test_timeout_raises_error(self, mock_xclip_backend):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="xclip", timeout=5)
            
            with pytest.raises(ClipboardTimeoutError):
                mock_xclip_backend.get_text()
    
    def test_get_available_formats_parses_targets(self, mock_xclip_backend):
        targets_output = "UTF8_STRING\ntext/plain\ntext/html\nimage/png\n"
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout=targets_output
            )
            
            formats = mock_xclip_backend.get_available_formats()
            
            from xclipboard import ClipboardFormat
            assert ClipboardFormat.PLAIN_TEXT in formats
            assert ClipboardFormat.HTML in formats
            assert ClipboardFormat.IMAGE in formats
    
    def test_clear_sends_empty_input(self, mock_xclip_backend):
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.returncode = 0
            mock_process.communicate.return_value = (b"", b"")
            mock_popen.return_value = mock_process
            
            mock_xclip_backend.clear()
            
            mock_process.communicate.assert_called_with(input=b"", timeout=5)


@skip_unless_linux
class TestLinuxBackendIntegration:
    """Integration tests for Linux backend (requires Linux with xclip)."""
    
    @pytest.fixture
    def linux_backend(self):
        if not shutil.which("xclip"):
            pytest.skip("xclip not installed")
        
        from xclipboard.backends.linux import LinuxClipboardBackend
        return LinuxClipboardBackend()
    
    def test_instantiation(self, linux_backend):
        assert linux_backend is not None
    
    def test_set_and_get_text(self, linux_backend):
        test_text = "Linux clipboard test"
        
        linux_backend.set_text(test_text)
        result = linux_backend.get_text()
        
        assert result == test_text
    
    def test_unicode_text(self, linux_backend):
        unicode_text = "Hello 世界 🌍"
        
        linux_backend.set_text(unicode_text)
        result = linux_backend.get_text()
        
        assert result == unicode_text
    
    def test_get_available_formats(self, linux_backend):
        linux_backend.set_text("test")
        
        formats = linux_backend.get_available_formats()
        assert isinstance(formats, list)
