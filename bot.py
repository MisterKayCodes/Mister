#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mister Kay - Your personal coding assistant
Usage: python bot.py <command> [arguments]
"""

import sys
import os

# Ensure UTF-8 output encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

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

  copy <file>     Copy file content to clipboard
                  Example: kay copy index.jsx
                  Example: kay copy src/app.py

  paste           Paste clipboard to last copied file
                  Example: kay paste
                  Example: kay paste newfile.txt
                  Example: kay paste --preview
                  Example: kay paste --undo

  listen          Show the last crash error in a nice format
                  Example: kay listen

  imports         Show broken imports in current project
                  Example: kay imports
                  Example: kay imports --fix (coming soon)

  todo            Find TODO, FIXME, and BUG comments
                  Example: kay todo

  check           Run project health check (syntax, dependencies, heavy files)
                  Example: kay check

  talk            Chat with Kay interactively in plain English!
                  Example: kay talk

  analyze         Parse a Python file and find its dependents
                  Example: kay analyze bot.py

  extract         Safely extract a class/function to a new file
                  Example: kay extract bot.py main new_file.py

  bundle          Bundle multiple files into a single clipboard string
                  Example: kay bundle file1.py file2.py

  apply           Apply file updates & terminal commands directly from clipboard
                  Example: kay apply [--force]

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

def command_imports():
    """Handle the 'imports' command"""
    from core.imports_brain import ImportsBrain
    
    path = os.getcwd()
    result = ImportsBrain.analyze_imports(path)
    
    # Format output
    print(f"\n📊 Import Analysis - {path}")
    print("=" * 50)
    print(f"📁 Files scanned: {result['files_scanned']}")
    print(f"📦 Total imports: {result['total_imports']}")
    print(f"✅ Valid imports: {result['valid_imports']}")
    print(f"❌ Broken imports: {result['broken_imports']}")
    print("=" * 50)
    
    if result['broken_imports'] == 0:
        print("\n🎉 No broken imports found! Your project is clean.")
    else:
        print("\n🔍 Broken imports:")
        for issue in result['issues']:
            print(f"\n   📄 {issue['file']}")
            print(f"      Line: {issue['line']}")
            print(f"      ❌ {issue['error']}")
        print(f"\n💡 Tip: Run 'kay imports --fix' to attempt auto-fix")

def command_copy(file_path):
    """Handle the 'copy' command"""
    
    if not file_path:
        print("❌ Error: Please provide a file to copy")
        print("Example: kay copy index.jsx")
        print("Example: kay copy src/app.py")
        return
    
    from core.clipboard_brain import ClipboardBrain
    success, message = ClipboardBrain.copy_file(file_path)
    print(message)

def command_paste(file_path=None, preview=False, undo=False):
    """Handle the 'paste' command"""
    
    from core.clipboard_brain import ClipboardBrain
    success, message = ClipboardBrain.paste_to_file(file_path, preview, undo)
    print(message)


def command_clean(dry_run=False, backups=False, temp=False):
    """Handle the 'clean' command"""
    from core.clean_brain import CleanBrain
    
    path = os.getcwd()
    
    if backups:
        if dry_run:
            count, message = CleanBrain.delete_backups(path, dry_run=True)
            print(f"\n🧹 DRY RUN - Found {count} .bak files")
            print("=" * 40)
            print(message)
            print("\n💡 Run 'kay clean --backups' to delete them")
        else:
            count, message = CleanBrain.delete_backups(path, dry_run=False)
            print(f"\n🧹 {message}")
    else:
        print("❌ Please specify what to clean")
        print("Example: kay clean --backups")
        print("Example: kay clean --backups --dry-run")

def command_todo():
    """Handle the 'todo' command"""
    from core.todo_brain import TodoBrain
    
    path = os.getcwd()
    result = TodoBrain.scan_todos(path)
    
    print(f"\n📋 Todo Scan - {path}")
    print("=" * 50)
    print(f"📁 Files scanned: {result['files_scanned']}")
    print(f"📌 Todos found: {result['todos_found']}")
    print("=" * 50)
    
    if result['todos_found'] == 0:
        print("\n🎉 No TODOs, FIXMEs, or BUGs found! Your code is spotless.")
    else:
        for file_path, todos in result['results']:
            print(f"\n📄 {file_path}:")
            for line_num, text in todos:
                print(f"   [{line_num}] {text}")

def command_check():
    """Handle the 'check' command"""
    from core.check_brain import CheckBrain
    
    path = os.getcwd()
    print(f"\n🩺 Running Project Health Check - {path}...")
    result = CheckBrain.run_check(path)
    
    print("=" * 50)
    print(f"📁 Python files scanned: {result['files_scanned']}")
    
    # Syntax Errors
    if result['syntax_errors']:
        print("\n❌ SYNTAX ERRORS FOUND:")
        for err in result['syntax_errors']:
            print(f"   📄 {err['file']}:{err['line']}")
            print(f"      {err['msg']}")
            if err['text']:
                print(f"      Code: {err['text']}")
    else:
        print("✅ Syntax: All clear! No broken code found.")
        
    # Heavy Files
    if result['heavy_files']:
        print("\n⚠️  HEAVY FILES DETECTED (>550 lines):")
        for file, lines in result['heavy_files']:
            print(f"   📄 {file} is getting huge ({lines} lines). Consider splitting it!")
    else:
        print("✅ File Size: All clear! No massive files found.")
        
    # Requirements
    if os.path.exists(os.path.join(path, 'requirements.txt')):
        if result['missing_requirements']:
            print("\n❌ MISSING REQUIREMENTS:")
            for req in result['missing_requirements']:
                print(f"   📦 You imported '{req}' but it's not in requirements.txt!")
                
        if result['unused_requirements']:
            print("\n👻 GHOST REQUIREMENTS:")
            for req in result['unused_requirements']:
                print(f"   👻 '{req}' is in requirements.txt but you aren't importing it.")
                
        if not result['missing_requirements'] and not result['unused_requirements']:
            print("✅ Dependencies: All clear! requirements.txt matches your imports perfectly.")
    else:
        print("\n⚠️  No requirements.txt found. Skipping dependency check.")
        
    print("=" * 50)

def command_chat():
    """Handle the 'talk' command"""
    from core.chat_brain import ChatBrain
    ChatBrain.start_chat()

def command_analyze(target_file):
    from core.analyze_brain import AnalyzeBrain
    import os
    path = os.getcwd()
    result = AnalyzeBrain.analyze_file(path, os.path.join(path, target_file))
    
    if "error" in result:
        print(f"❌ {result['error']}")
        return
        
    print(f"\n🔍 Blueprint for {target_file}")
    print("=" * 50)
    for c in result['classes']:
        print(f"📦 Class: {c['name']} (Lines {c['start']}-{c['end']})")
    for f in result['functions']:
        print(f"🔧 Function: {f['name']} (Lines {f['start']}-{f['end']})")
        
    if not result['dependents']:
        print("\n✅ No other files depend on this file.")
    else:
        print("\n⚠️  The following files depend on this file:")
        for d in result['dependents']:
            print(f"   - {d}")
    print("=" * 50)

def command_extract(source_file, target_name, dest_file):
    from core.extract_brain import ExtractBrain
    import os
    path = os.getcwd()
    success, msg = ExtractBrain.extract_node(
        os.path.join(path, source_file),
        target_name,
        os.path.join(path, dest_file)
    )
    print(f"{'✅' if success else '❌'} {msg}")

def command_bundle(file_paths):
    from core.bundle_brain import BundleBrain
    import os
    
    # Convert paths to absolute if they aren't already
    path = os.getcwd()
    abs_paths = [os.path.join(path, f) for f in file_paths]
    
    success, msg, missing = BundleBrain.bundle_files(abs_paths)
    
    if success:
        print(f"✅ Bundled {len(file_paths) - len(missing)} files and copied to clipboard!")
        if missing:
            print("⚠️ The following files were skipped (not found or error):")
            for m in missing:
                print(f"   - {m}")
    else:
        print(msg)

def command_apply(force):
    from core.patch_brain import PatchBrain
    success, msg = PatchBrain.parse_and_apply(force=force)
    print(msg)

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
    
    elif command == "copy":
        from parsers import parse_copy
        file_path, error = parse_copy(sys.argv)
        
        if error:
            print(f"❌ Error: {error}")
            print("Example: kay copy index.jsx")
            print("Example: kay copy src/app.py")
        else:
            command_copy(file_path)
    
    elif command == "paste":
        from parsers import parse_paste
        file_path, preview, undo, error = parse_paste(sys.argv)
        
        if error:
            print(f"❌ Error: {error}")
        else:
            command_paste(file_path, preview, undo)
    
    elif command == "listen":
        from parsers import parse_listen
        if not parse_listen(sys.argv):
            print("❌ Error: 'kay listen' takes no arguments")
            print("Example: kay listen")
        else:
            command_listen()
    
    elif command == "imports":
        from parsers import parse_imports
        show_fix = parse_imports(sys.argv)
        
        if show_fix:
            # TODO: Add --fix functionality in next step
            print("🔧 --fix coming soon!")
        else:
            command_imports()

    elif command == "clean":
        from parsers import parse_clean
        dry_run, backups, temp = parse_clean(sys.argv)
        
        if not backups and not temp:
            print("❌ Please specify what to clean")
            print("Example: kay clean --backups")
        else:
            command_clean(dry_run, backups, temp)
            
    elif command == "todo":
        from parsers import parse_todo
        parse_todo(sys.argv)
        command_todo()
        
    elif command == "check":
        from parsers import parse_check
        parse_check(sys.argv)
        command_check()
        
    elif command == "talk":
        from parsers import parse_chat
        parse_chat(sys.argv)
        command_chat()
        
    elif command == "analyze":
        from parsers import parse_analyze
        target_file = parse_analyze(sys.argv)
        if not target_file:
            print("❌ Error: Please provide a file to analyze")
            print("Example: kay analyze bot.py")
        else:
            command_analyze(target_file)
            
    elif command == "extract":
        from parsers import parse_extract
        source_file, target_name, dest_file = parse_extract(sys.argv)
        if not source_file:
            print("❌ Error: Missing arguments")
            print("Example: kay extract bot.py command_chat new.py")
        else:
            command_extract(source_file, target_name, dest_file)
            
    elif command == "teach":
        from parsers import parse_teach
        word, intent = parse_teach(sys.argv)
        if not word:
            print("❌ Error: Missing arguments")
            print("Example: kay teach yoink extract")
        else:
            from core.teach_brain import TeachBrain
            if TeachBrain.save_vocab(word, intent):
                print(f"✅ I will remember that '{word}' means '{intent}'!")
            else:
                print("❌ Failed to save memory.")

    elif command == "bundle":
        from parsers import parse_bundle
        file_paths = parse_bundle(sys.argv)
        if not file_paths:
            print("❌ Error: Please provide at least one file to bundle.")
            print("Example: kay bundle bot.py core/chat_brain.py")
        else:
            command_bundle(file_paths)
            
    elif command == "apply":
        from parsers import parse_apply
        force = parse_apply(sys.argv)
        command_apply(force)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Type 'python bot.py help' for available commands")

if __name__ == "__main__":
    main()