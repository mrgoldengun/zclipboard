"""Windows (Win32) clipboard backend implementation."""

import ctypes
from ctypes import wintypes
from io import BytesIO
from typing import List, Optional

from xclipboard.backends.base import ClipboardBackend
from xclipboard.data_types import ClipboardFormat
from xclipboard.exceptions import ClipboardAccessError

# Win32 Constants
CF_BITMAP = 2
CF_DIB = 8
CF_DIBV5 = 17
CF_TEXT = 1
CF_UNICODETEXT = 13
GHND = 0x0042
GMEM_MOVEABLE = 0x0002

# Win32 API Functions
kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

CloseClipboard = user32.CloseClipboard
EmptyClipboard = user32.EmptyClipboard
EnumClipboardFormats = user32.EnumClipboardFormats
GetClipboardData = user32.GetClipboardData
GetClipboardData.restype = ctypes.c_void_p
GlobalAlloc = kernel32.GlobalAlloc
GlobalAlloc.restype = ctypes.c_void_p
GlobalLock = kernel32.GlobalLock
GlobalLock.argtypes = [ctypes.c_void_p]
GlobalLock.restype = ctypes.c_void_p
GlobalSize = kernel32.GlobalSize
GlobalSize.argtypes = [ctypes.c_void_p]
GlobalSize.restype = ctypes.c_size_t
GlobalUnlock = kernel32.GlobalUnlock
GlobalUnlock.argtypes = [ctypes.c_void_p]
OpenClipboard = user32.OpenClipboard
OpenClipboard.argtypes = [wintypes.HWND]
RegisterClipboardFormatW = user32.RegisterClipboardFormatW
RegisterClipboardFormatW.argtypes = [wintypes.LPCWSTR]
RegisterClipboardFormatW.restype = ctypes.c_uint
SetClipboardData = user32.SetClipboardData
SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]


class WindowsClipboardBackend(ClipboardBackend):
    """Windows clipboard backend using Win32 API."""
    
    def __init__(self):
        self._cf_html = RegisterClipboardFormatW("HTML Format")
        self._cf_rtf = RegisterClipboardFormatW("Rich Text Format")
        self._cf_png = RegisterClipboardFormatW("PNG")
    
    def _close_clipboard(self) -> None:
        CloseClipboard()
    
    def _get_clipboard_data(self, format_id: int) -> Optional[bytes]:
        handle = GetClipboardData(format_id)
        if not handle:
            return None
        
        ptr = GlobalLock(handle)
        if not ptr:
            return None
        
        try:
            size = GlobalSize(handle)
            data = ctypes.string_at(ptr, size)
            return data
        finally:
            GlobalUnlock(handle)
    
    def _open_clipboard(self) -> None:
        for _ in range(10):
            if OpenClipboard(None):
                return
            ctypes.windll.kernel32.Sleep(10)
        raise ClipboardAccessError("Failed to open clipboard")
    
    def _set_clipboard_data(self, format_id: int, data: bytes) -> None:
        handle = GlobalAlloc(GMEM_MOVEABLE, len(data))
        if not handle:
            raise ClipboardAccessError("Failed to allocate global memory")
        
        ptr = GlobalLock(handle)
        if not ptr:
            raise ClipboardAccessError("Failed to lock global memory")
        
        try:
            ctypes.memmove(ptr, data, len(data))
        finally:
            GlobalUnlock(handle)
        
        if not SetClipboardData(format_id, handle):
            raise ClipboardAccessError("Failed to set clipboard data")
    
    def clear(self) -> None:
        try:
            self._open_clipboard()
            EmptyClipboard()
        finally:
            self._close_clipboard()
    
    def get_available_formats(self) -> List[ClipboardFormat]:
        formats = []
        try:
            self._open_clipboard()
            format_id = EnumClipboardFormats(0)
            while format_id:
                if format_id == CF_UNICODETEXT:
                    formats.append(ClipboardFormat.PLAIN_TEXT)
                elif format_id == self._cf_html:
                    formats.append(ClipboardFormat.HTML)
                elif format_id == self._cf_rtf:
                    formats.append(ClipboardFormat.RTF)
                elif format_id in (CF_DIB, CF_DIBV5, self._cf_png):
                    if ClipboardFormat.IMAGE not in formats:
                        formats.append(ClipboardFormat.IMAGE)
                format_id = EnumClipboardFormats(format_id)
        finally:
            self._close_clipboard()
        return formats
    
    def get_html(self) -> Optional[str]:
        try:
            self._open_clipboard()
            data = self._get_clipboard_data(self._cf_html)
            if data:
                return self._parse_html_format(data.decode("utf-8", errors="ignore"))
            return None
        finally:
            self._close_clipboard()
    
    def get_image(self) -> Optional[bytes]:
        try:
            self._open_clipboard()
            png_data = self._get_clipboard_data(self._cf_png)
            if png_data:
                return png_data
            dib_data = self._get_clipboard_data(CF_DIBV5) or self._get_clipboard_data(CF_DIB)
            if dib_data:
                return self._convert_dib_to_png(dib_data)
            return None
        finally:
            self._close_clipboard()
    
    def get_rtf(self) -> Optional[str]:
        try:
            self._open_clipboard()
            data = self._get_clipboard_data(self._cf_rtf)
            if data:
                return data.decode("utf-8", errors="ignore").rstrip("\x00")
            return None
        finally:
            self._close_clipboard()
    
    def get_text(self) -> Optional[str]:
        try:
            self._open_clipboard()
            data = self._get_clipboard_data(CF_UNICODETEXT)
            if data:
                return data.decode("utf-16-le", errors="ignore").rstrip("\x00")
            return None
        finally:
            self._close_clipboard()
    
    def set_html(self, html_content: str, plain_text_fallback: Optional[str] = None) -> None:
        html_format = self._create_html_format(html_content)
        try:
            self._open_clipboard()
            EmptyClipboard()
            self._set_clipboard_data(self._cf_html, html_format.encode("utf-8") + b"\x00")
            if plain_text_fallback:
                self._set_clipboard_data(CF_UNICODETEXT, (plain_text_fallback + "\x00").encode("utf-16-le"))
        finally:
            self._close_clipboard()
    
    def set_image(self, image_data: bytes) -> None:
        try:
            self._open_clipboard()
            EmptyClipboard()
            self._set_clipboard_data(self._cf_png, image_data)
            dib_data = self._convert_png_to_dib(image_data)
            if dib_data:
                self._set_clipboard_data(CF_DIB, dib_data)
        finally:
            self._close_clipboard()
    
    def set_rtf(self, rtf_content: str, plain_text_fallback: Optional[str] = None) -> None:
        try:
            self._open_clipboard()
            EmptyClipboard()
            self._set_clipboard_data(self._cf_rtf, rtf_content.encode("utf-8") + b"\x00")
            if plain_text_fallback:
                self._set_clipboard_data(CF_UNICODETEXT, (plain_text_fallback + "\x00").encode("utf-16-le"))
        finally:
            self._close_clipboard()
    
    def set_text(self, text: str) -> None:
        try:
            self._open_clipboard()
            EmptyClipboard()
            self._set_clipboard_data(CF_UNICODETEXT, (text + "\x00").encode("utf-16-le"))
        finally:
            self._close_clipboard()
    
    def _convert_dib_to_png(self, dib_data: bytes) -> Optional[bytes]:
        """Convert DIB data to PNG format."""
        try:
            from PIL import Image
            bmp_header = b"BM" + len(dib_data).to_bytes(4, "little") + b"\x00\x00\x00\x00" + b"\x36\x00\x00\x00"
            bmp_data = bmp_header + dib_data
            img = Image.open(BytesIO(bmp_data))
            output = BytesIO()
            img.save(output, format="PNG")
            return output.getvalue()
        except ImportError:
            return dib_data
    
    def _convert_png_to_dib(self, png_data: bytes) -> Optional[bytes]:
        """Convert PNG data to DIB format."""
        try:
            from PIL import Image
            img = Image.open(BytesIO(png_data))
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            output = BytesIO()
            img.save(output, format="BMP")
            bmp_data = output.getvalue()
            return bmp_data[14:]
        except ImportError:
            return None
    
    def _create_html_format(self, html_content: str) -> str:
        """Create Windows HTML clipboard format."""
        header_template = (
            "Version:0.9\r\n"
            "StartHTML:{start_html:010d}\r\n"
            "EndHTML:{end_html:010d}\r\n"
            "StartFragment:{start_fragment:010d}\r\n"
            "EndFragment:{end_fragment:010d}\r\n"
        )
        prefix = "<!DOCTYPE html><html><body><!--StartFragment-->"
        suffix = "<!--EndFragment--></body></html>"
        
        header_length = len(header_template.format(
            start_html=0, end_html=0, start_fragment=0, end_fragment=0
        ))
        
        start_html = header_length
        start_fragment = start_html + len(prefix)
        end_fragment = start_fragment + len(html_content.encode("utf-8"))
        end_html = end_fragment + len(suffix)
        
        header = header_template.format(
            start_html=start_html,
            end_html=end_html,
            start_fragment=start_fragment,
            end_fragment=end_fragment,
        )
        
        return header + prefix + html_content + suffix
    
    def _parse_html_format(self, html_format: str) -> str:
        """Parse Windows HTML clipboard format and extract the HTML fragment."""
        start_marker = "<!--StartFragment-->"
        end_marker = "<!--EndFragment-->"
        
        start_idx = html_format.find(start_marker)
        end_idx = html_format.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            return html_format[start_idx + len(start_marker):end_idx]
        return html_format
