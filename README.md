
# 🧠 Mister - Your Personal Coding Assistant

**Mister** is a lightweight, terminal-based AI assistant that lives in your project folder. No API calls. No token costs. Just pure Python that helps you scan, understand, and navigate your codebase.

> *"Stop burning money on LLMs. Let Mister do the simple stuff."*

---

## ✨ Features

### Current Capabilities

| Command | What it does |
|---------|---------------|
| `kay scan [path]` | Shows folder tree with smart depth control |
| `kay help` | Displays this help message |

### Smart Scanning Behavior

- **≤50 items** → Shows full folder tree automatically
- **>50 items** → Shows root level, then asks "Show all files? (y/n)"
- **Auto-skips** → `venv`, `.git`, `node_modules`, `__pycache__`, and more
- **Current folder** → Type `kay scan` without a path to scan where you are

---

## 🚀 Quick Start

### Installation

1. **Clone or download Mister** to `C:\Kaycris\Mister`

2. **Add to PATH** (run PowerShell as Administrator):
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Kaycris\Mister", [EnvironmentVariableTarget]::Machine)
   ```

3. **Restart your terminal**

### Usage

```bash
# Scan any folder
kay scan C:\MyProject

# Scan current folder
cd C:\MyProject
kay scan

# Show help
kay help
```

---

## 📁 Project Structure

```
Mister/
├── bot.py                 # 🦴 Skeleton + Mouth (CLI entry point)
├── kay.bat                # 🖐️ Terminal launcher
├── core/
│   └── tree_brain.py      # 🧠 Brain (scanning logic)
├── tools/
│   └── file_walker.py     # Hands (file system access)
├── memory/                # 💾 Memory (future: learned patterns)
├── docs/
│   └── capabilities.md    # 📋 Full command reference
└── README.md              # This file
```

### Biological Architecture (Mister Alert inspired)

| Component | Role | Location |
|-----------|------|----------|
| 🧠 Brain | Pure logic, no I/O | `core/` |
| 🖐️ Hands | File system actions | `tools/` |
| 👄 Mouth | CLI parsing | `bot.py` |
| 🦴 Skeleton | App entry & wiring | `bot.py` |
| 💾 Memory | Persistent storage | `memory/` |

---

## 🧪 Examples

### Small folder (≤50 items) - Auto full scan

```bash
$ kay scan C:\Kaycris\Mister_FC

📁 Scanning: C:\Kaycris\Mister_FC
--------------------------------------------------
📁 C:\Kaycris\Mister_FC/
├── 📄 convert.py
├── 📄 extract_players.py
├── 📁 Converted_PNGs/
│   ├── 📄 IMG_5009.png
│   └── 📄 IMG_5010.png
└── 📁 photos/
    ├── 📄 IMG_5009.jpeg
    └── 📄 IMG_5010.jpeg
```

### Large folder (>50 items) - Asks before full scan

```bash
$ kay scan C:\LargeProject

📁 Scanning: C:\LargeProject
--------------------------------------------------
📁 C:\LargeProject/
├── 📄 README.md
├── 📁 src/
├── 📁 tests/
└── 📁 assets/
--------------------------------------------------
📊 This folder has 156 items (more than 50).
❓ Show all files? (y/n): y

[shows full tree]
```

---

## 🔧 Skipped Folders (Auto-Ignored)

Mister automatically skips these to keep output clean:

- `.git`
- `node_modules`
- `__pycache__`
- `venv`, `.venv`, `env`
- `.mypy_cache`, `.pytest_cache`
- `Lib`, `Scripts`, `share` (virtual environment junk)

---

## 📝 Roadmap

- [x] `kay scan` - Smart folder tree
- [x] 50-item threshold with prompt
- [x] Current folder detection
- [x] Global `kay` command (PATH)
- [ ] `kay read <file>` - Show file contents
- [ ] `kay find "<text>"` - Search across files
- [ ] `kay teach "<pattern>"` - Learn new patterns
- [ ] `kay remember` - Show learned patterns
- [ ] `kay watch` - Watch for file changes

---

## ❓ FAQ

### Why not just use an LLM?

LLMs cost money per token. Mister costs $0. It handles the repetitive tasks (scanning, finding, reading) that don't need AI.

### Why "Mister"?

Short for **Mister Alert** - the biological architecture this project is built on. Every file has a purpose: Brain, Hands, Mouth, Memory.

### Does Mister use AI?

**Not yet.** Phase 1 is pure Python. Phase 2 will integrate local LLMs (Ollama, GPT4All) for teaching and learning.

### Can I teach Mister new things?

**Soon!** The `teach` command is in development. You'll be able to show Mister patterns once, and it will remember them forever.

---

## 🧠 Built On

- **Python 3.11+** - Pure Python, no external dependencies
- **Mister Alert Architecture** - Biological code organization
- **Your Feedback** - Built for developers, by a developer

---

## 📄 License

MIT - Do whatever you want with it.

---

## 🙏 Credits

Inspired by the **Mister Alert** biological architecture (Brain, Mouth, Hands, Memory). Built because LLM tokens are crazy expensive.

---

**Made with 🧠 by Kay** | [Report Issue](https://github.com/misterkaycodes/mister/issues)
```

-