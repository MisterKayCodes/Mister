#!/usr/bin/env python3
"""
Mister Kay - Your personal coding assistant
Usage: python bot.py <command> [arguments]
"""

import sys
import os

# Add the current directory to path so we can import core
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_help():
    """Show available commands"""
    print("""
📋 Mister Kay - Available Commands:

  scan [path]     Show folder tree of [path]
                  If no path given, scans current folder
                  Example: python bot.py scan C:/myproject
                  Example: python bot.py scan

  read <file>     Show contents of a file
                  Example: kay read bot.py
                  Example: kay read bot.py --lines
                  Example: kay read bot.py 10-25
                  Example: kay read bot.py 10-25 --lines

  help            Show this message

More commands coming: teach, find, remember
""")

def command_scan(path):
    """Handle the 'scan' command"""
    
    if not path:
        path = os.getcwd()
        print(f"📁 No path specified. Scanning current folder: {path}")
    
    if not os.path.exists(path):
        print(f"❌ Error: Path does not exist: {path}")
        return
    
    if not os.path.isdir(path):
        print(f"❌ Error: Path is not a folder: {path}")
        return
    
    from core.tree_brain import TreeBrain
    # Use the new smart scan with prompt
    TreeBrain.scan_with_prompt(path)

# ============================================
# UPDATED: read command handler with line range
# ============================================
def command_read(file_path, show_lines=False, line_range=None):
    """Handle the 'read' command"""
    
    if not file_path:
        print("❌ Error: Please provide a file to read")
        print("Example: kay read bot.py")
        print("Example: kay read bot.py --lines")
        print("Example: kay read bot.py 10-25")
        return
    
    from core.reader_brain import ReaderBrain
    result = ReaderBrain.read_file(file_path, show_lines, line_range)
    print(result)
# ============================================

def main():
    """The Mouth - parses what you say"""
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
    
    elif command == "scan":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        command_scan(path)
    
    # ============================================
    # UPDATED: read command with line range parsing
    # ============================================
    elif command == "read":
        if len(sys.argv) < 3:
            print("❌ Error: Please provide a file to read")
            print("Example: kay read bot.py")
            print("Example: kay read bot.py --lines")
            print("Example: kay read bot.py 10-25")
        else:
            file_path = sys.argv[2]
            show_lines = "--lines" in sys.argv
            
            # Check for line range (e.g., "10-25")
            line_range = None
            for arg in sys.argv[3:]:
                if "-" in arg and not arg.startswith("--"):
                    try:
                        parts = arg.split("-")
                        start = int(parts[0])
                        end = int(parts[1])
                        line_range = (start, end)
                    except:
                        print(f"❌ Invalid line range: {arg}")
                        print("Use format like: 10-25")
                        return
            
            command_read(file_path, show_lines, line_range)
    # ============================================
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Type 'python bot.py help' for available commands")

if __name__ == "__main__":
    main()