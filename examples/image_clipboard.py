"""Example: Image clipboard operations."""

from pathlib import Path

from xclipboard import Clipboard, ClipboardFormat


def main():
    clipboard = Clipboard()
    
    # Example 1: Set image from file
    image_path = Path("sample_image.png")
    
    if image_path.exists():
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        clipboard.set_image(image_data)
        print("Image set to clipboard from file")
    else:
        # Create a simple test image using PIL (if available)
        try:
            from io import BytesIO

            from PIL import Image
            
            img = Image.new("RGB", (100, 100), color="red")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            image_data = buffer.getvalue()
            
            clipboard.set_image(image_data)
            print("Test image (red 100x100) set to clipboard")
        except ImportError:
            print("PIL not available. Please install Pillow: pip install Pillow")
            print("Or provide a sample_image.png file in the current directory.")
            return
    
    # Check if image is available
    if clipboard.has_format(ClipboardFormat.IMAGE):
        print("Image format is available on clipboard")
        
        # Get image from clipboard
        retrieved_image = clipboard.get_image()
        if retrieved_image:
            output_path = Path("retrieved_image.png")
            with open(output_path, "wb") as f:
                f.write(retrieved_image)
            print(f"Image retrieved and saved to: {output_path}")
    else:
        print("No image format available on clipboard")


if __name__ == "__main__":
    main()
