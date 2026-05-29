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

  listen          Show the last crash error in a nice format
                  Example: kay listen

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
    TreeBrain.scan_with_prompt(path)

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

def command_find(search_term, extensions=None, ignore_case=False, context_lines=0, count_only=False):
    """Handle the 'find' command"""
    
    if not search_term:
        print("❌ Error: Please provide a search term")
        return
    
    path = os.getcwd()
    
    from core.find_brain import FindBrain
    result = FindBrain.search_with_prompt(path, search_term, extensions, ignore_case, context_lines, count_only)
    print(result)

def command_listen():
    """Handle the 'listen' command"""
    from core.listen_brain import ListenBrain
    result = ListenBrain.get_crash_report()
    print(result)

def main():
    """The Mouth - parses what you say"""
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
    
    elif command == "scan":
        from parsers import parse_scan
        path = parse_scan(sys.argv)
        command_scan(path)
    
    elif command == "read":
        from parsers import parse_read
        file_path, show_lines, line_range = parse_read(sys.argv)
        
        if line_range == "invalid_range":
            print("❌ Invalid line range. Use format like: 10-25")
        elif file_path is None:
            print("❌ Error: Please provide a file to read")
            print("Example: kay read bot.py")
            print("Example: kay read bot.py --lines")
            print("Example: kay read bot.py 10-25")
        else:
            command_read(file_path, show_lines, line_range)
    
    elif command == "find":
        from parsers import parse_find
        search_term, extensions, ignore_case, context_lines, count_only = parse_find(sys.argv)
        
        if context_lines == "invalid_context":
            print("❌ Invalid context value. Use format like: --context 2")
        elif search_term is None:
            print("❌ Error: Please provide a search term")
            print("Example: kay find import")
            print("Example: kay find import --ext .py")
            print("Example: kay find import --ignore-case")
            print("Example: kay find import --context 2")
            print("Example: kay find import --count")
        else:
            command_find(search_term, extensions, ignore_case, context_lines, count_only)
    
    elif command == "listen":
        from parsers import parse_listen
        if not parse_listen(sys.argv):
            print("❌ Error: 'kay listen' takes no arguments")
            print("Example: kay listen")
        else:
            command_listen()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Type 'python bot.py help' for available commands")

if __name__ == "__main__":
    main()