
# Mister Kay - Complete User Guide

## 📋 All Commands

### scan
- **Usage:** `kay scan [path]`
- **What it does:** Shows folder tree
- **Smart behavior:** ≤50 items → full tree, >50 items → asks "show all?"
- **Skips:** venv, .git, node_modules, __pycache__, etc.

### read
- **Usage:** `kay read <file>`
- **Options:** `--lines` (line numbers), `10-25` (line range)
- **Smart behavior:** Auto-detects missing files, folders, binary files

### find
- **Usage:** `kay find <term>`
- **Options:** `--ext .py`, `--ignore-case`, `--count`
- **Default extensions:** .py, .txt, .md, .json, .yml, .csv

### copy
- **Usage:** `kay copy <file>`
- **What it does:** Copies file content to clipboard
- **Smart behavior:** Uses tkinter + temp file fallback, remembers last copied file

### paste
- **Usage:** `kay paste [file]`
- **Options:** `--preview` (show first 20 lines), `--undo` (restore from backup)
- **Smart behavior:** Creates `.bak` backup before overwriting

### imports
- **Usage:** `kay imports`
- **What it does:** Analyzes Python imports, finds broken dependencies
- **Shows:** Files scanned, total imports, valid/broken count

### clean
- **Usage:** `kay clean --backups`
- **Options:** `--dry-run` (preview what would be deleted)
- **What it does:** Deletes all `.bak` files recursively

### listen
- **Usage:** `kay listen`
- **What it does:** Shows last crash error in nice format

### kay_run
- **Usage:** `kay_run python main.py`
- **What it does:** Runs file, auto-captures crashes for `kay listen`

### todo
- **Usage:** `kay todo`
- **What it does:** Scans project for TODO, FIXME, and BUG comments
- **Smart behavior:** Only checks text and code files, skipping binaries and ignore directories.

### check
- **Usage:** `kay check`
- **What it does:** Runs project health check.
- **Smart behavior:**
  - **Syntax Sweep:** Checks all Python files for fatal syntax errors without executing them.
  - **Dependency Detective:** Compares your `import` statements against `requirements.txt` to find missing or unused packages.
  - **Heavy File Warning:** Warns you if any file exceeds 550 lines.

### talk
- **Usage:** `kay talk`
- **What it does:** Opens an interactive chat loop.
- **Smart behavior:** Uses keyword mapping to secretly run commands (`check`, `todo`, `imports`, `scan`) and responds with a randomized, dynamic personality engine. If he doesn't understand you, he enters Learning Mode to ask you what you meant and remembers it forever.

### analyze
- **Usage:** `kay analyze <file>`
- **What it does:** Scans a target Python file and maps out all its classes and functions.
- **Smart behavior:** Also scans the rest of the project to find any files that currently import the target file so you know what will break if you move things.

### extract
- **Usage:** `kay extract <source> <name> <dest>`
- **What it does:** Surgical copy-pasting. Safely extracts the target class/function from the source file and writes it to the destination file.
- **Smart behavior:** Leaves the original file intact (Safe Mode) so you can manually delete it when you are confident.

### teach
- **Usage:** `kay teach <word> <intent>`
- **What it does:** Hardcodes a custom synonym into Kay's brain.
- **Example:** `kay teach "take out" "extract"`

### bundle
- **Usage:** `kay bundle <file1> <file2> ...`
- **What it does:** Reads multiple files, adds a markdown header with the filename for each, separates them with `------------------`, and copies the entire bundled string to your clipboard.
- **Smart behavior:** Perfect for feeding context to AI models. If a file is missing, he will let you know instead of crashing.

### apply
- **Usage:** `kay apply [--force]`
- **What it does:** The ultimate AI sync tool. Reads your clipboard for specially formatted DeepSeek answers (using `@@FILE:` and `@@CMD`), previews the changes, and automatically overwrites your local files and runs the terminal commands.
- **Smart behavior:** Checks if the new code is perfectly identical or suspiciously shorter than the old code and warns you first!

## 🧪 Examples

```bash
# Scan
kay scan
kay scan C:\Project

# Read
kay read bot.py
kay read bot.py --lines
kay read bot.py 10-25

# Find
kay find import
kay find import --ext .py
kay find import --count

# Copy/Paste
kay copy bot.py
kay paste newfile.py
kay paste --preview
kay paste --undo

# Imports
kay imports

# Todo
kay todo

# Check
kay check

# Talk
kay talk

# Analyze & Extract
kay analyze bot.py
kay extract bot.py command_chat chat_logic.py
kay teach yoink extract

# Bundle
kay bundle bot.py core/chat_brain.py core/check_brain.py

# Apply
kay apply
kay apply --force

# Clean
kay clean --backups --dry-run
kay clean --backups

# Crash capture
kay_run python main.py
kay listen
```

## 📁 Full Project Structure

```
Mister/
├── bot.py
├── kay.bat
├── kay_run.bat
├── parsers/
│   ├── scan_parser.py
│   ├── read_parser.py
│   ├── find_parser.py
│   ├── clipboard_parser.py
│   ├── listen_parser.py
│   ├── imports_parser.py
│   ├── clean_parser.py
│   ├── todo_parser.py
│   ├── check_parser.py
│   └── chat_parser.py
├── core/
│   ├── tree_brain.py
│   ├── reader_brain.py
│   ├── find_brain.py
│   ├── clipboard_brain.py
│   ├── listen_brain.py
│   ├── imports_brain.py
│   ├── clean_brain.py
│   ├── todo_brain.py
│   ├── check_brain.py
│   ├── chat_brain.py
│   └── personality_engine.py
├── tools/
│   ├── file_walker.py
│   ├── error_catcher.py
│   └── clipboard_helper.py
├── memory/
│   ├── last_error.txt
│   └── clipboard_history.json
└── docs/
    └── FULL_GUIDE.md
```

## 🔧 Skipped Folders (Auto-Ignored)

`.git`, `node_modules`, `__pycache__`, `venv`, `.venv`, `env`, `.mypy_cache`, `.pytest_cache`, `Lib`, `Scripts`, `share`

## 📝 Roadmap

- [x] scan, read, find, copy, paste, imports, clean, listen
- [x] todo
- [x] check
- [x] talk (Interactive Chat)
- [x] analyze & extract (Refactoring)
- [x] teach command
- [x] bundle & apply (LLM Sync)
- [ ] `--fix` for imports
- [ ] `--context` for find
- [ ] `teach` command
- [ ] Parallel search

## ❓ FAQ

**Why not use an LLM?** Cost. Mister is free.

**Does Mister use AI?** Not yet. Phase 2 will add local LLMs.

**How to update Mister?** `git pull`

**Where are backups saved?** Same folder as original file with `.bak` extension.
```

---

