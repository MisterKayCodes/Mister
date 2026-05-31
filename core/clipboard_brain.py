"""Clipboard Brain - handles copy/paste logic"""

import os
import json
import shutil
import tempfile
from tools.clipboard_helper import ClipboardHelper


class ClipboardBrain:
    """Brain - pure logic for copy/paste operations"""
    
    MEMORY_FILE = "memory/clipboard_history.json"
    TEMP_CLIPBOARD_FILE = None  # Will be set in _ensure_memory
    
    @staticmethod
    def _ensure_memory():
        """Ensure memory file exists"""
        if not os.path.exists(ClipboardBrain.MEMORY_FILE):
            os.makedirs(os.path.dirname(ClipboardBrain.MEMORY_FILE), exist_ok=True)
            
            # Create temp clipboard file in temp directory
            temp_dir = tempfile.gettempdir()
            ClipboardBrain.TEMP_CLIPBOARD_FILE = os.path.join(temp_dir, "mister_clipboard_content.txt")
            
            with open(ClipboardBrain.MEMORY_FILE, 'w') as f:
                json.dump({
                    "last_copied_file": None, 
                    "history": [],
                    "clipboard_temp_file": ClipboardBrain.TEMP_CLIPBOARD_FILE
                }, f)
    
    @staticmethod
    def _load_memory():
        """Load clipboard memory"""
        ClipboardBrain._ensure_memory()
        try:
            with open(ClipboardBrain.MEMORY_FILE, 'r') as f:
                data = json.load(f)
                # Set temp file path from memory
                ClipboardBrain.TEMP_CLIPBOARD_FILE = data.get("clipboard_temp_file")
                return data
        except:
            return {"last_copied_file": None, "history": []}
    
    @staticmethod
    def _save_memory(data):
        """Save clipboard memory"""
        ClipboardBrain._ensure_memory()
        with open(ClipboardBrain.MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def _store_clipboard_content(content):
        """Store clipboard content in temp file for inter-process access"""
        try:
            temp_file = os.path.join(tempfile.gettempdir(), "mister_clipboard_content.txt")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return temp_file
        except:
            return None
    
    @staticmethod
    def _read_clipboard_content():
        """Read clipboard content from Windows clipboard FIRST, then temp file fallback"""
        
        # FIXED: Method 1 - Check Windows clipboard FIRST (latest manual copy)
        direct_content = ClipboardHelper.paste_from_clipboard()
        if direct_content and len(direct_content.strip()) > 0:
            # Update temp file with this new content for future use
            ClipboardBrain._store_clipboard_content(direct_content)
            return direct_content
        
        # Method 2 - Fallback to temp file (what kay copy saved)
        try:
            temp_file = os.path.join(tempfile.gettempdir(), "mister_clipboard_content.txt")
            if os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except:
            pass
        
        return None
    
    @staticmethod
    def copy_file(file_path):
        """
        Copy file content to clipboard and remember it
        
        Args:
            file_path: path to file
            
        Returns:
            tuple: (success: bool, message: str)
        """
        
        # Check if file exists
        if not os.path.exists(file_path):
            return False, f"❌ File not found: {file_path}"
        
        # Check if it's a file
        if os.path.isdir(file_path):
            return False, f"❌ That's a folder, not a file: {file_path}"
        
        # Check if it's a text file (simple heuristic)
        binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.exe', '.bin', '.dat', '.pyc'}
        _, ext = os.path.splitext(file_path)
        if ext.lower() in binary_extensions:
            return False, f"❌ Cannot copy binary file: {file_path}"
        
        # Read file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            return False, f"❌ Cannot copy binary file: {file_path}"
        except Exception as e:
            return False, f"❌ Error reading file: {e}"
        
        # Copy to clipboard
        if not ClipboardHelper.copy_to_clipboard(content):
            return False, f"❌ Failed to copy to clipboard"
        
        # Also store in temp file for inter-process access
        ClipboardBrain._store_clipboard_content(content)
        
        # Save to memory
        memory = ClipboardBrain._load_memory()
        # Convert to absolute path for consistency
        abs_path = os.path.abspath(file_path)
        memory["last_copied_file"] = abs_path
        if abs_path not in memory["history"]:
            memory["history"].append(abs_path)
        ClipboardBrain._save_memory(memory)
        
        # Calculate stats
        line_count = len(content.splitlines())
        size_kb = len(content.encode('utf-8')) / 1024
        
        return True, f"📋 Copied {line_count} lines ({size_kb:.1f} KB) from {file_path}\n✅ Ready to paste (Ctrl+V)"
    
    @staticmethod
    def paste_to_file(file_path=None, preview=False, undo=False):
        """
        Paste clipboard content to file
        
        Args:
            file_path: optional target file path
            preview: if True, show preview instead of writing
            undo: if True, restore from backup
            
        Returns:
            tuple: (success: bool, message: str)
        """
        
        # Handle undo
        if undo:
            memory = ClipboardBrain._load_memory()
            target = file_path or memory.get("last_copied_file")
            
            if not target:
                return False, "❌ No file to undo"
            
            backup_path = target + ".bak"
            if not os.path.exists(backup_path):
                return False, f"❌ No backup found for {target}"
            
            try:
                shutil.copy2(backup_path, target)
                return True, f"✅ Restored {target} from backup"
            except Exception as e:
                return False, f"❌ Error restoring backup: {e}"
        
        # Get clipboard content (NOW reads Windows clipboard first)
        clipboard_content = ClipboardBrain._read_clipboard_content()
        if not clipboard_content:
            return False, "❌ Nothing to paste. Copy something first."
        
        # Determine target file
        if file_path:
            target = file_path
        else:
            memory = ClipboardBrain._load_memory()
            target = memory.get("last_copied_file")
            if not target:
                return False, "❌ No last copied file. Specify file: kay paste <file>"
        
        # Handle preview
        if preview:
            lines = clipboard_content.splitlines()
            preview_lines = lines[:20]
            preview_text = "\n".join(preview_lines)
            
            if len(lines) > 20:
                preview_text += f"\n\n... and {len(lines) - 20} more lines"
            
            return True, f"🔍 Preview ({len(lines)} lines total):\n\n{preview_text}"
        
        # Create backup if file exists
        if os.path.exists(target):
            backup_path = target + ".bak"
            try:
                shutil.copy2(target, backup_path)
                backup_msg = f"\n💾 Backup saved: {target}.bak"
            except Exception as e:
                return False, f"❌ Error creating backup: {e}"
        else:
            backup_msg = ""
        
        # Write file
        try:
            os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
            with open(target, 'w', encoding='utf-8') as f:
                f.write(clipboard_content)
        except Exception as e:
            return False, f"❌ Error writing to file: {e}"
        
        # Calculate stats
        line_count = len(clipboard_content.splitlines())
        
        return True, f"✅ Pasted {line_count} lines to {target}{backup_msg}"
    
    @staticmethod
    def get_last_copied_file():
        """Get the last copied file path"""
        memory = ClipboardBrain._load_memory()
        return memory.get("last_copied_file")