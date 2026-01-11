"""MacOS (Cocoa) clipboard backend implementation."""

from io import BytesIO
from typing import List, Optional

from xclipboard.backends.base import ClipboardBackend
from xclipboard.data_types import ClipboardFormat
from xclipboard.exceptions import ClipboardAccessError

try:
    import objc
    from AppKit import (
        NSPasteboard,
        NSPasteboardTypeHTML,
        NSPasteboardTypePNG,
        NSPasteboardTypeRTF,
        NSPasteboardTypeString,
        NSPasteboardTypeTIFF,
    )
    PYOBJC_AVAILABLE = True
except ImportError:
    PYOBJC_AVAILABLE = False

NSPasteboardTypeRTFD = "com.apple.flat-rtfd" if PYOBJC_AVAILABLE else None


class MacOSClipboardBackend(ClipboardBackend):
    """MacOS clipboard backend using Cocoa/PyObjC."""
    
    def __init__(self):
        if not PYOBJC_AVAILABLE:
            raise ClipboardAccessError(
                "PyObjC is required for MacOS clipboard support. "
                "Install it with: pip install pyobjc-framework-Cocoa"
            )
        self._pasteboard = NSPasteboard.generalPasteboard()
    
    def clear(self) -> None:
        self._pasteboard.clearContents()
    
    def get_available_formats(self) -> List[ClipboardFormat]:
        formats = []
        types = self._pasteboard.types()
        
        if types is None:
            return formats
        
        if NSPasteboardTypeString in types:
            formats.append(ClipboardFormat.PLAIN_TEXT)
        if NSPasteboardTypeHTML in types:
            formats.append(ClipboardFormat.HTML)
        if NSPasteboardTypeRTF in types or NSPasteboardTypeRTFD in types:
            formats.append(ClipboardFormat.RTF)
        if NSPasteboardTypePNG in types or NSPasteboardTypeTIFF in types:
            formats.append(ClipboardFormat.IMAGE)
        
        return formats
    
    def get_html(self) -> Optional[str]:
        data = self._pasteboard.dataForType_(NSPasteboardTypeHTML)
        if data:
            return bytes(data).decode("utf-8", errors="ignore")
        return None
    
    def get_image(self) -> Optional[bytes]:
        png_data = self._pasteboard.dataForType_(NSPasteboardTypePNG)
        if png_data:
            return bytes(png_data)
        
        tiff_data = self._pasteboard.dataForType_(NSPasteboardTypeTIFF)
        if tiff_data:
            return self._convert_tiff_to_png(bytes(tiff_data))
        
        return None
    
    def get_rtf(self) -> Optional[str]:
        data = self._pasteboard.dataForType_(NSPasteboardTypeRTF)
        if data:
            return bytes(data).decode("utf-8", errors="ignore")
        return None
    
    def get_text(self) -> Optional[str]:
        return self._pasteboard.stringForType_(NSPasteboardTypeString)
    
    def set_html(self, html_content: str, plain_text_fallback: Optional[str] = None) -> None:
        self._pasteboard.clearContents()
        
        types_to_declare = [NSPasteboardTypeHTML]
        if plain_text_fallback:
            types_to_declare.append(NSPasteboardTypeString)
        
        self._pasteboard.declareTypes_owner_(types_to_declare, None)
        self._pasteboard.setData_forType_(
            html_content.encode("utf-8"),
            NSPasteboardTypeHTML
        )
        
        if plain_text_fallback:
            self._pasteboard.setString_forType_(plain_text_fallback, NSPasteboardTypeString)
    
    def set_image(self, image_data: bytes) -> None:
        self._pasteboard.clearContents()
        self._pasteboard.declareTypes_owner_([NSPasteboardTypePNG], None)
        self._pasteboard.setData_forType_(image_data, NSPasteboardTypePNG)
    
    def set_rtf(self, rtf_content: str, plain_text_fallback: Optional[str] = None) -> None:
        self._pasteboard.clearContents()
        
        types_to_declare = [NSPasteboardTypeRTF]
        if plain_text_fallback:
            types_to_declare.append(NSPasteboardTypeString)
        
        self._pasteboard.declareTypes_owner_(types_to_declare, None)
        self._pasteboard.setData_forType_(
            rtf_content.encode("utf-8"),
            NSPasteboardTypeRTF
        )
        
        if plain_text_fallback:
            self._pasteboard.setString_forType_(plain_text_fallback, NSPasteboardTypeString)
    
    def set_text(self, text: str) -> None:
        self._pasteboard.clearContents()
        self._pasteboard.declareTypes_owner_([NSPasteboardTypeString], None)
        self._pasteboard.setString_forType_(text, NSPasteboardTypeString)
    
    def _convert_tiff_to_png(self, tiff_data: bytes) -> Optional[bytes]:
        """Convert TIFF data to PNG format."""
        try:
            from PIL import Image
            img = Image.open(BytesIO(tiff_data))
            output = BytesIO()
            img.save(output, format="PNG")
            return output.getvalue()
        except ImportError:
            return tiff_data
