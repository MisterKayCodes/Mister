"""Clipboard Helper - Hands for copy/paste operations using pyperclip"""

import os
import tempfile


class ClipboardHelper:
    """Handles clipboard operations using pyperclip + temp file fallback"""
    
    @staticmethod
    def copy_to_clipboard(text):
        """
        Copy text to clipboard using pyperclip.
        Returns True if successful.
        """
        # Method 1: Try pyperclip
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except ImportError:
            print("   ⚠️ pyperclip not installed. Run: pip install pyperclip")
        except Exception as e:
            print(f"   ⚠️ pyperclip error: {e}")
        
        # Method 2: Fallback to temp file
        return ClipboardHelper._copy_to_temp_file(text)
    
    @staticmethod
    def _copy_to_temp_file(text):
        """Save to temp file as last resort"""
        try:
            temp_file = os.path.join(tempfile.gettempdir(), "mister_clipboard_content.txt")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"   📁 Content saved to: {temp_file}")
            print("   Open this file and press Ctrl+A, Ctrl+C to copy")
            return True
        except Exception:
            return False
    
    @staticmethod
    def paste_from_clipboard():
        """
        Get text from clipboard using pyperclip.
        Returns text or None if failed.
        """
        # Method 1: Try pyperclip
        try:
            import pyperclip
            text = pyperclip.paste()
            if text:
                return text
        except ImportError:
            pass
        except Exception:
            pass
        
        # Method 2: Try temp file
        return ClipboardHelper._paste_from_temp_file()
    
    @staticmethod
    def _paste_from_temp_file():
        """Read from temp file"""
        try:
            temp_file = os.path.join(tempfile.gettempdir(), "mister_clipboard_content.txt")
            if os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception:
            pass
        return None
    
    @staticmethod
    def clear_clipboard():
        """Clear the clipboard"""
        try:
            import pyperclip
            pyperclip.copy("")
            return True
        except Exception:
            return False