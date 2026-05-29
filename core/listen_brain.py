"""Listen Brain - Knows how to read and format crash errors"""

import os
from tools.error_catcher import get_last_error, has_error

class ListenBrain:
    """Brain - formats error messages nicely"""
    
    @staticmethod
    def get_crash_report():
        """Get the last crash error formatted nicely"""
        
        # Check if there's an error saved
        if not has_error():
            return "📭 No crash detected yet.\n\nRun something with 'kay_run' first, then try 'kay listen'."
        
        # Get the error
        error_text = get_last_error()
        
        if not error_text:
            return "❌ Error file is empty."
        
        # Format nicely
        result = "\n🔍 Last Crash Report\n"
        result += "=" * 50 + "\n\n"
        
        # Try to extract the actual error message (last line is usually the error)
        lines = error_text.strip().split('\n')
        
        # Find the error line (usually starts with ModuleNotFoundError, FileNotFoundError, etc.)
        error_line = None
        for line in reversed(lines):
            if ': ' in line and ('Error' in line or 'error' in line):
                error_line = line.strip()
                break
        
        if error_line:
            result += f"❌ Error: {error_line}\n\n"
        else:
            # Show last few lines if can't find specific error
            result += "❌ Error details:\n"
            for line in lines[-5:]:
                result += f"   {line}\n"
            result += "\n"
        
        # Show full traceback (optional - first few lines)
        result += "📋 Full traceback (last 10 lines):\n"
        result += "-" * 30 + "\n"
        for line in lines[-10:]:
            result += f"   {line}\n"
        
        result += "\n" + "=" * 50 + "\n"
        result += "💡 Tip: Type 'kay teach' to teach me about this error.\n"
        
        return result
    
    @staticmethod
    def get_error_summary():
        """Just get the error type and message (no traceback)"""
        
        if not has_error():
            return None
        
        error_text = get_last_error()
        lines = error_text.strip().split('\n')
        
        # Find the error line
        for line in reversed(lines):
            if ': ' in line and ('Error' in line or 'error' in line):
                return line.strip()
        
        return lines[-1] if lines else None