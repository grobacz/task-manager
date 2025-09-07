# Task Tracker - Linux Windowed Application

## Project Overview
A lightweight Linux desktop application that displays tasks from a markdown file in a resizable window. Users can interact with checkboxes to mark tasks as complete, automatically updating the source markdown file.

## Current Implementation Status: ✅ COMPLETE

### Core Features (Implemented)
- ✅ **Task Display**: Renders markdown checklist items (`- [ ]` / `- [x]`) as interactive checkboxes
- ✅ **Real-time File Updates**: Checkbox interactions immediately modify source markdown file
- ✅ **Smart Window Sizing**: Automatically resizes window to fit content on file load
- ✅ **Always on Top**: Toggle button with wmctrl integration for X11 window managers
- ✅ **File Persistence**: Remembers last opened file and window preferences
- ✅ **Modern UI**: Icon-based toolbar with tooltips, strikethrough for completed tasks

### Advanced Features (Implemented)
1. **Settings Management**: Persistent configuration in `~/.config/task-tracker/settings.json`
2. **Screen Bounds Protection**: Window sizing constrained to 80% of screen dimensions
3. **Content-Aware Sizing**: Height/width calculated based on task count and text length
4. **GTK4 Modern APIs**: Uses FileDialog (not deprecated FileChooserDialog)
5. **System Integration**: Native file dialogs, system icons, theme compliance

## Technical Implementation

### Technology Stack (Final)
- ✅ **Framework**: GTK4 with Python (PyGObject) - Native Linux integration
- ✅ **File Handling**: Python `pathlib` and `re` for markdown parsing  
- ✅ **Window Manager Integration**: `wmctrl` for X11 always-on-top functionality
- ✅ **Settings Storage**: JSON configuration files
- ✅ **Modern APIs**: GTK4 FileDialog, GIO ListStore, async patterns

### Implemented Components
1. ✅ **TaskParser** (`task_parser.py`): Regex-based markdown parsing with file I/O
2. ✅ **TaskTrackerWindow** (`main.py`): GTK4 UI with dynamic content sizing
3. ✅ **Settings** (`settings.py`): Persistent configuration management
4. ✅ **Smart Resizing**: Content-aware window dimensions with screen constraints
5. ✅ **Native Integration**: System icons, file dialogs, theme compliance

## Current File Structure
```
task-tracker/
├── src/
│   ├── main.py           # GTK4 application and UI
│   ├── task_parser.py    # Markdown parsing and file operations  
│   └── settings.py       # Configuration persistence
├── requirements.txt      # Python dependencies
├── Makefile             # Setup automation
├── tasks.md             # Sample task file
└── CLAUDE.md           # This documentation
```

## Usage
```bash
# Setup (one-time)
make install

# Run application
make run
# or directly: python src/main.py
```

## Requirements
- **OS**: Linux with X11 (tested on Ubuntu/GNOME)
- **Dependencies**: GTK4, Python 3.x, wmctrl
- **Python Packages**: PyGObject, watchdog

## Technical Notes
- **Task Pattern**: `^(\s*)-\s\[([ x])\]\s(.+)$` for markdown parsing
- **Configuration**: `~/.config/task-tracker/settings.json`
- **Window Sizing**: Base 45px + (tasks × 22px) + spacing, max 80% screen
- **Always On Top**: Requires wmctrl and X11 window manager
- **File Persistence**: Auto-saves last opened file and window preferences

## Known Limitations
- X11 only (Wayland support would require different always-on-top approach)
- No file watching for external changes (manual reload via file dialog)
- No keyboard shortcuts implemented
- No system tray integration