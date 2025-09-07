# Task Tracker

A lightweight Linux desktop application that displays and manages markdown task lists with interactive checkboxes.

## Quick Start

```bash
# Install dependencies
make install

# Run the application
make run
```

## Usage

1. **First Run**: The app will load `tasks.md` from the current directory if it exists
2. **Open Files**: Click the folder icon (📁) to open any markdown file with task lists
3. **Check Tasks**: Click checkboxes to mark tasks complete - changes save automatically
4. **Always on Top**: Click the pin icon (📌) to keep window above other applications
5. **Auto-Resize**: Window automatically adjusts size when loading different files

## Task Format

Your markdown files should contain tasks in this format:
```markdown
- [ ] Uncompleted task
- [x] Completed task
```

## Requirements

- Linux with X11 (Ubuntu, Fedora, etc.)
- Python 3.x and GTK4
- wmctrl (for always-on-top functionality)