import os

# ============================================
# ReaderBrain with line range support
# ============================================

class ReaderBrain:
    """Brain - knows how to read and display files"""
    
    @staticmethod
    def read_file(file_path, show_lines=False, line_range=None):
        """
        Read file and return formatted content
        
        Args:
            file_path: path to file
            show_lines: if True, show line numbers
            line_range: tuple (start, end) or None for all lines
        """
        
        # Check if file exists
        if not os.path.exists(file_path):
            return f"❌ Error: File not found - {file_path}"
        
        # Check if it's a file (not a folder)
        if os.path.isdir(file_path):
            return f"❌ Error: That's a folder, not a file - {file_path}"
        
        # Try to read the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            return f"❌ Error: Cannot read binary file - {file_path}"
        except Exception as e:
            return f"❌ Error: {e}"
        
        # ============================================
        # Apply line range if specified
        # ============================================
        total_lines = len(lines)
        
        if line_range:
            start, end = line_range
            # Convert to 0-index and adjust bounds
            start_idx = max(0, start - 1)
            end_idx = min(total_lines, end)
            lines = lines[start_idx:end_idx]
            start_line = start
        else:
            start_line = 1
        # ============================================
        
        # Build the output
        result = f"\n📄 {file_path}\n"
        
        # ============================================
        # Show range info if specific lines requested
        # ============================================
        if line_range:
            result += f"📌 Lines {start} to {end} (total {total_lines} lines in file)\n"
        result += "=" * 50 + "\n"
        # ============================================
        
        for i, line in enumerate(lines, start=start_line):
            if show_lines:
                result += f"{i:4d} | {line.rstrip()}\n"
            else:
                result += line
        
        # ============================================
        # If no lines in range, say so
        # ============================================
        if line_range and not lines:
            result = f"\n📄 {file_path}\n"
            result += f"❌ No lines found in range {start}-{end}. File has {total_lines} lines.\n"
        # ============================================
        
        return result