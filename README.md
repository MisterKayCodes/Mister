
# 🧠 Mister - Your Personal Coding Assistant

> *"Stop burning money on LLMs. Let Mister do the simple stuff."*

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-windows-lightgrey)]()

**Mister** is a lightweight, terminal-based assistant that lives in your project folder. It handles the repetitive tasks you'd normally ask an LLM for — scanning folders, reading files, searching code, copying to clipboard, analyzing imports — without spending a single token.

Perfect for developers who are tired of paying for simple operations that should be instant and free.

---

## ✨ Features

| Command | What it does |
|---------|---------------|
| `kay scan` | Smart folder tree (asks before huge folders) |
| `kay read` | Read files with line numbers and ranges |
| `kay find` | Search across files with extension filters |
| `kay copy` | Copy file to clipboard (works across terminals) |
| `kay paste` | Paste with automatic backup and undo |
| `kay imports` | Find broken Python imports |
| `kay clean --backups` | Delete all .bak files recursively |
| `kay listen` | View last crash error in nice format |
| `kay todo` | Find TODO, FIXME, and BUG comments in code |
| `kay check` | Project health check (syntax, dependencies, heavy files) |
| `kay talk` | Chat with Kay interactively in plain English |
| `kay analyze` | Map out a file's blueprint and dependencies |
| `kay extract` | Safely copy a class/function to a new file |
| `kay teach` | Teach him new synonyms |
| `kay bundle` | Combine multiple files into a single clipboard string for LLMs |

---

## 🚀 Quick Install

### 1. Clone or download
```bash
git clone https://github.com/misterkaycodes/mister.git C:\Kaycris\Mister
# Or just copy the files manually
```

### 2. Add to PATH (PowerShell as Administrator)
```bash
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Kaycris\Mister", [EnvironmentVariableTarget]::Machine)
```

### 3. Install dependency
```bash
py -m pip install pyperclip
```

### 4. Restart your terminal

### 5. Test it
```bash
kay scan
# Should show the folder tree of current directory
```

---

## 📖 Usage Examples

```bash
# Scan current folder
kay scan

# Read a file with line numbers
kay read bot.py --lines

# Search all Python files for "import"
kay find import --ext .py

# Copy a file to clipboard
kay copy bot.py

# Paste to a new file
kay paste newfile.py

# Preview before pasting
kay paste --preview

# Undo last paste
kay paste --undo

# Check for broken imports
kay imports

# Find all TODO and FIXME comments
kay todo

# Run project health check
kay check

# Chat with Kay interactively
kay talk

# Clean up backup files (preview first)
kay clean --backups --dry-run
kay clean --backups

# Run with crash capture
kay_run python main.py

# View last crash
kay listen
```

---

## 🧪 Example Output

```bash
$ kay scan

📁 Scanning: C:\Kaycris\Mister
--------------------------------------------------
📁 C:\Kaycris\Mister/
├── 📄 bot.py
├── 📄 kay.bat
├── 📁 core/
│   └── 📄 tree_brain.py
└── 📁 tools/
    └── 📄 file_walker.py

$ kay copy bot.py

📋 Copied 246 lines (7.9 KB) from bot.py
✅ Ready to paste (Ctrl+V)
```

---

## 📋 Requirements

- **Python 3.11+** (3.13 recommended)
- **Windows** (Linux/Mac coming soon)
- **pyperclip** (installed automatically above)

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `'kay' is not recognized` | Restart terminal after PATH change |
| `pip not found` | Use `py -m pip install pyperclip` |
| `kay paste does nothing` | Run `kay paste --preview` to see clipboard content |
| `ModuleNotFoundError` | Run `kay imports` to find broken imports |

---

## 📚 Full Documentation

See [docs/FULL_GUIDE.md](docs/FULL_GUIDE.md) for:
- All command options and flags
- Smart behavior explanations
- Project architecture
- Roadmap and FAQ

---

## 📄 License

MIT — Do whatever you want with it.

---

**Made with 🧠 by Kay** | [Report Issue](https://github.com/misterkaycodes/mister/issues)
```