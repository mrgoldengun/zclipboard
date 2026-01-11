"""Example: RTF (Rich Text Format) clipboard operations."""

from xclipboard import Clipboard


def main():
    clipboard = Clipboard()
    
    # Create RTF content
    rtf_content = r"""{\rtf1\ansi\deff0
{\fonttbl{\f0 Arial;}}
\f0\fs24 This is \b bold\b0  and this is \i italic\i0  text.
\par
This is a second paragraph with {\ul underlined} text.
}"""
    
    plain_text_fallback = "This is bold and this is italic text.\nThis is a second paragraph with underlined text."
    
    # Set RTF content
    clipboard.set_rtf(rtf_content, plain_text_fallback)
    print("RTF content set to clipboard")
    
    # Get RTF content
    retrieved_rtf = clipboard.get_rtf()
    print(f"Retrieved RTF: {retrieved_rtf[:100]}..." if retrieved_rtf else "No RTF content")
    
    # Get plain text fallback
    retrieved_text = clipboard.get_text()
    print(f"Retrieved text fallback: {retrieved_text}")


if __name__ == "__main__":
    main()
