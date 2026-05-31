
# Mister Kay - Capabilities

## Current Commands

### scan
- **Usage:** `kay scan [path]`
- **What it does:** Shows folder tree
- **Smart behavior:** 
   - ≤50 items → full tree
   - >50 items → root only, asks "show all?"
- **Skips:** venv, .git, node_modules, __pycache__, etc.

### read
- **Usage:** `kay read <file>`
- **What it does:** Shows file contents in the terminal
- **Options:**
   - `kay read bot.py` → Shows entire file
   - `kay read bot.py --lines` → Shows file with line numbers
   - `kay read bot.py 10-25` → Shows only lines 10 to 25
   - `kay read bot.py 10-25 --lines` → Shows lines 10-25 with numbers
- **Smart behavior:**
   - Auto-detects if file exists
   - Won't crash on binary files (images, videos)
   - Shows "file not found" if missing
   - Shows "that's a folder" if you try to read a folder
   - Shows line range info when using specific lines
- **Skips:** Binary files (can't read them)

### find
- **Usage:** `kay find <search_term>`
- **What it does:** Searches for text across all files in current folder
- **Options:**
   - `kay find import` → Basic search (default extensions)
   - `kay find import --ext .py` → Only search Python files
   - `kay find import --ext .py --ext .js` → Search multiple extensions
   - `kay find import --ignore-case` → Case insensitive search
   - `kay find import --count` → Show only match count (no line details)
   - `kay find import --context 2` → Show 2 lines before/after match (coming soon)
- **Smart behavior:**
   - Auto-skips venv, .git, node_modules, etc.
   - Shows file path, line number, and matching line
   - Won't crash on binary/unreadable files
   - Shows search summary (total matches, files searched)
- **Default extensions:** .py, .txt, .md, .json, .yml, .yaml, .csv, .ini, .cfg, .toml
- **Skips:** Same folders as scan + binary files

### copy
- **Usage:** `kay copy <file>`
- **What it does:** Copies file content to clipboard
- **Smart behavior:**
   - Uses tkinter for reliable cross-process clipboard access
   - Falls back to temp file if tkinter unavailable
   - Shows line count and file size
   - Remembers last copied file in memory
   - Auto-detects binary files (won't copy)
- **Example output:**
```
📋 Copied 246 lines (7.9 KB) from bot.py
✅ Ready to paste (Ctrl+V)
```

### paste
- **Usage:** `kay paste [file]`
- **What it does:** Pastes clipboard content to file
- **Options:**
   - `kay paste newfile.py` → Paste to new file
   - `kay paste` → Paste to last copied file (auto-remembers)
   - `kay paste --preview` → Show first 20 lines before pasting
   - `kay paste --undo` → Restore from backup file
- **Smart behavior:**
   - Always creates `.bak` backup before overwriting
   - Works in separate terminal sessions (inter-process safe)
   - Remembers clipboard content across process restarts
   - Easy undo via `--undo` flag
- **Example output:**
```
✅ Pasted 246 lines to bot.py
💾 Backup saved: bot.py.bak
```

### imports
- **Usage:** `kay imports`
- **What it does:** Analyzes Python imports and finds broken dependencies
- **Smart behavior:**
   - Scans all Python files in current folder
   - Reports total imports, valid imports, broken imports
   - Shows exact line number and file for each broken import
   - Auto-skips same folders as scan
   - Fast analysis (single pass)
- **Example output:**
```
📊 Import Analysis - C:\Project
==================================================
📁 Files scanned: 12
📦 Total imports: 45
✅ Valid imports: 43
❌ Broken imports: 2
==================================================

🔍 Broken imports:

   📄 services/api_client.py
      Line: 8
      ❌ No module named 'requests'

   📄 utils/logger.py
      Line: 3
      ❌ No module named 'loguru'

💡 Tip: Run 'kay imports --fix' to attempt auto-fix
```

### listen
- **Usage:** `kay listen`
- **What it does:** Shows the last crash error in a nice format
- **How it works:**
   - Run `kay_run python your_file.py` to auto-capture crashes
   - Or manually save errors with `save_error()`
   - Then `kay listen` displays the formatted error
- **Smart behavior:**
   - Extracts the main error message from traceback
   - Shows full traceback (last 10 lines)
   - Suggests "kay teach" for unknown errors
- **Example output:**
```
🔍 Last Crash Report
==================================================
❌ Error: ModuleNotFoundError: No module named 'loguru'

📋 Full traceback (last 10 lines):
------------------------------
   File "main.py", line 16, in <module>
     from loguru import logger
ModuleNotFoundError: No module named 'loguru'
==================================================
💡 Tip: Type 'kay teach' to teach me about this error.
```

### kay_run (wrapper)
- **What it does:** Wrapper script that runs your Python files and auto-captures crashes
- **Usage:** `kay_run python main.py`
- **How it works:**
   - Runs any command
   - If crash occurs → auto-saves error to memory
   - Then `kay listen` can show the error
   - If success → runs normally, no error saved
- **Works from any folder** (if PATH is set)

### help
- **Usage:** `kay help`
- **What it does:** Shows available commands

## Coming Soon
- `kay paste --fix` - Auto-fix import issues
- `kay listen --fix` - Auto-suggest fixes for errors
- `kay teach` - Teach Mister about new errors
- `kay find --context` - Show surrounding lines (in progress)
- `kay remember` - Show what I've learned
- Parallel search (faster for large projects)

## Known Limitations
- Only reads text files (no binary/image files)
- Max depth for scan: unlimited (but asks for large folders)
- Line numbers start at 1 (not 0)
- File encoding assumes UTF-8
- Find command is single-threaded (may be slow on 10,000+ files)
- Context lines feature not yet fully implemented

---
