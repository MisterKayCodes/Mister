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

  find <term>     Search for text in files
                  Example: kay find import
                  Example: kay find import --ext .py
                  Example: kay find import --ignore-case
                  Example: kay find import --context 2
                  Example: kay find import --count

  help            Show this message

More commands coming: teach, remember
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
# read command handler with line range
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

# ============================================
# NEW: find command handler
# ============================================
def command_find(search_term, extensions=None, ignore_case=False, context_lines=0, count_only=False):
    """Handle the 'find' command"""
    
    if not search_term:
        print("❌ Error: Please provide a search term")
        return
    
    path = os.getcwd()  # Search current folder by default
    
    from core.find_brain import FindBrain
    result = FindBrain.search_with_prompt(path, search_term, extensions, ignore_case, context_lines, count_only)
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
    # read command with line range parsing
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
    
    # ============================================
    # NEW: find command
    # ============================================
    elif command == "find":
        if len(sys.argv) < 3:
            print("❌ Error: Please provide a search term")
            print("Example: kay find import")
            print("Example: kay find import --ext .py")
            print("Example: kay find import --ignore-case")
            print("Example: kay find import --context 2")
            print("Example: kay find import --count")
        else:
            search_term = sys.argv[2]
            
            # Parse options
            extensions = None
            ignore_case = False
            context_lines = 0
            count_only = False
            
            i = 3
            while i < len(sys.argv):
                arg = sys.argv[i]
                
                if arg == "--ext" and i + 1 < len(sys.argv):
                    ext = sys.argv[i + 1]
                    if not ext.startswith('.'):
                        ext = '.' + ext
                    if extensions is None:
                        extensions = {ext}
                    else:
                        extensions.add(ext)
                    i += 2
                
                elif arg == "--ignore-case":
                    ignore_case = True
                    i += 1
                
                elif arg == "--context" and i + 1 < len(sys.argv):
                    try:
                        context_lines = int(sys.argv[i + 1])
                    except:
                        print(f"❌ Invalid context value: {sys.argv[i + 1]}")
                        return
                    i += 2
                
                elif arg == "--count":
                    count_only = True
                    i += 1
                
                elif arg.startswith("--"):
                    print(f"❌ Unknown option: {arg}")
                    i += 1
                
                else:
                    i += 1
            
            command_find(search_term, extensions, ignore_case, context_lines, count_only)
    # ============================================
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Type 'python bot.py help' for available commands")

if __name__ == "__main__":
    main()