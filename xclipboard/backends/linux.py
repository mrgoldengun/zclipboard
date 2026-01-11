"""Linux (XClip) clipboard backend implementation."""

import shutil
import subprocess
from io import BytesIO
from typing import List, Optional

from xclipboard.backends.base import ClipboardBackend
from xclipboard.data_types import ClipboardFormat
from xclipboard.exceptions import ClipboardAccessError, ClipboardTimeoutError

XCLIP_TIMEOUT = 5


class LinuxClipboardBackend(ClipboardBackend):
    """Linux clipboard backend using xclip command-line tool."""
    
    MIME_HTML = "text/html"
    MIME_IMAGE_PNG = "image/png"
    MIME_RTF = "text/rtf"
    MIME_TEXT = "text/plain"
    MIME_UTF8 = "UTF8_STRING"
    
    def __init__(self):
        self._xclip_path = shutil.which("xclip")
        if not self._xclip_path:
            raise ClipboardAccessError(
                "xclip is required for Linux clipboard support. "
                "Install it with: sudo apt-get install xclip (Debian/Ubuntu) "
                "or sudo dnf install xclip (Fedora)"
            )
    
    def _get_clipboard_data(self, target: str) -> Optional[bytes]:
        """Get clipboard data for a specific target/mime type."""
        try:
            result = subprocess.run(
                [self._xclip_path, "-selection", "clipboard", "-target", target, "-o"],
                capture_output=True,
                timeout=XCLIP_TIMEOUT,
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout
            return None
        except subprocess.TimeoutExpired:
            raise ClipboardTimeoutError("Clipboard operation timed out")
        except Exception:
            return None
    
    def _get_available_targets(self) -> List[str]:
        """Get list of available clipboard targets."""
        try:
            result = subprocess.run(
                [self._xclip_path, "-selection", "clipboard", "-target", "TARGETS", "-o"],
                capture_output=True,
                text=True,
                timeout=XCLIP_TIMEOUT,
            )
            if result.returncode == 0:
                return result.stdout.strip().split("\n")
            return []
        except Exception:
            return []
    
    def _set_clipboard_data(self, target: str, data: bytes) -> None:
        """Set clipboard data for a specific target/mime type."""
        try:
            process = subprocess.Popen(
                [self._xclip_path, "-selection", "clipboard", "-target", target, "-i"],
                stdin=subprocess.PIPE,
            )
            process.communicate(input=data, timeout=XCLIP_TIMEOUT)
            if process.returncode != 0:
                raise ClipboardAccessError(f"Failed to set clipboard data for target: {target}")
        except subprocess.TimeoutExpired:
            process.kill()
            raise ClipboardTimeoutError("Clipboard operation timed out")
    
    def clear(self) -> None:
        try:
            process = subprocess.Popen(
                [self._xclip_path, "-selection", "clipboard", "-i"],
                stdin=subprocess.PIPE,
            )
            process.communicate(input=b"", timeout=XCLIP_TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            raise ClipboardTimeoutError("Clipboard operation timed out")
    
    def get_available_formats(self) -> List[ClipboardFormat]:
        formats = []
        targets = self._get_available_targets()
        
        for target in targets:
            target_lower = target.lower()
            if "text/plain" in target_lower or "utf8_string" in target_lower or "string" == target_lower:
                if ClipboardFormat.PLAIN_TEXT not in formats:
                    formats.append(ClipboardFormat.PLAIN_TEXT)
            elif "text/html" in target_lower:
                if ClipboardFormat.HTML not in formats:
                    formats.append(ClipboardFormat.HTML)
            elif "text/rtf" in target_lower or "richtext" in target_lower:
                if ClipboardFormat.RTF not in formats:
                    formats.append(ClipboardFormat.RTF)
            elif "image/png" in target_lower or "image/jpeg" in target_lower or "image/bmp" in target_lower:
                if ClipboardFormat.IMAGE not in formats:
                    formats.append(ClipboardFormat.IMAGE)
        
        return formats
    
    def get_html(self) -> Optional[str]:
        data = self._get_clipboard_data(self.MIME_HTML)
        if data:
            return data.decode("utf-8", errors="ignore")
        return None
    
    def get_image(self) -> Optional[bytes]:
        png_data = self._get_clipboard_data(self.MIME_IMAGE_PNG)
        if png_data:
            return png_data
        
        for mime_type in ["image/jpeg", "image/bmp", "image/tiff"]:
            image_data = self._get_clipboard_data(mime_type)
            if image_data:
                return self._convert_image_to_png(image_data, mime_type)
        
        return None
    
    def get_rtf(self) -> Optional[str]:
        data = self._get_clipboard_data(self.MIME_RTF)
        if data:
            return data.decode("utf-8", errors="ignore")
        return None
    
    def get_text(self) -> Optional[str]:
        data = self._get_clipboard_data(self.MIME_UTF8)
        if data:
            return data.decode("utf-8", errors="ignore")
        
        data = self._get_clipboard_data(self.MIME_TEXT)
        if data:
            return data.decode("utf-8", errors="ignore")
        
        return None
    
    def set_html(self, html_content: str, plain_text_fallback: Optional[str] = None) -> None:
        self._set_clipboard_data(self.MIME_HTML, html_content.encode("utf-8"))
        if plain_text_fallback:
            self._set_clipboard_data(self.MIME_UTF8, plain_text_fallback.encode("utf-8"))
    
    def set_image(self, image_data: bytes) -> None:
        self._set_clipboard_data(self.MIME_IMAGE_PNG, image_data)
    
    def set_rtf(self, rtf_content: str, plain_text_fallback: Optional[str] = None) -> None:
        self._set_clipboard_data(self.MIME_RTF, rtf_content.encode("utf-8"))
        if plain_text_fallback:
            self._set_clipboard_data(self.MIME_UTF8, plain_text_fallback.encode("utf-8"))
    
    def set_text(self, text: str) -> None:
        self._set_clipboard_data(self.MIME_UTF8, text.encode("utf-8"))
    
    def _convert_image_to_png(self, image_data: bytes, mime_type: str) -> Optional[bytes]:
        """Convert image data to PNG format."""
        try:
            from PIL import Image
            img = Image.open(BytesIO(image_data))
            output = BytesIO()
            img.save(output, format="PNG")
            return output.getvalue()
        except ImportError:
            return image_data
