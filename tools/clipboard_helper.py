"""Clipboard Helper - Hands for copy/paste operations"""

import os
import tempfile
import tkinter as tk


class ClipboardHelper:
    """Handles clipboard operations (cross-platform via tkinter + temp file fallback)"""
    
    @staticmethod
    def copy_to_clipboard(text):
        """
        Copy text to clipboard using tkinter (primary) or temp file fallback.
        Returns True if successful.
        """
        # Method 1: Try tkinter (built-in, reliable, cross-platform)
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the window
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()  # Ensure clipboard is updated
            root.destroy()
            return True
        except Exception:
            pass
        
        # Method 2: Fallback to temp file (ensures data persists across processes)
        try:
            temp_file = os.path.join(tempfile.gettempdir(), "mister_clipboard_content.txt")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception:
            pass
        
        return False
    
    @staticmethod
    def paste_from_clipboard():
        """
        Get text from clipboard using tkinter (primary) or temp file fallback.
        Returns text or None if failed.
        """
        # Method 1: Try tkinter first (built-in, direct)
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the window
            text = root.clipboard_get()
            root.destroy()
            if text:
                return text
        except Exception:
            pass
        
        # Method 2: Fallback to temp file
        try:
            temp_file = os.path.join(tempfile.gettempdir(), "mister_clipboard_content.txt")
            if os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        return content
        except Exception:
            pass
        
        return None
    
    @staticmethod
    def clear_clipboard():
        """Clear the clipboard"""
        try:
            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.update()
            root.destroy()
            return True
        except Exception:
            return False