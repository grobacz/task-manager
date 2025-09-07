# Task Tracker

A lightweight Linux desktop application that displays and manages markdown task lists with interactive checkboxes.

## Quick Start

### Option 1: Download Pre-built Release (Easiest)
1. Go to [Releases](../../releases) and download the latest `task-tracker` executable
2. Make it executable: `chmod +x task-tracker`
3. Run: `./task-tracker`

### Option 2: Build Standalone Executable
```bash
# Build standalone executable (requires GTK4 system packages)
make build

# Run the standalone executable 
./dist/task-tracker
```

### Option 3: Run from Source
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

### For Standalone Executable
- Linux with X11 (Ubuntu, Fedora, etc.)
- GTK4 system libraries (usually pre-installed)
- wmctrl (for always-on-top functionality): `sudo apt install wmctrl`

### For Building from Source  
- Python 3.x and GTK4 development packages
- All dependencies from requirements.txt

## Releases & Distribution

### Automated Releases
- **GitHub Actions**: Automatically builds executables on every master push and creates releases on version tags
- **Development Builds**: Every master push creates test artifacts (7-day retention)
- **Release Builds**: Version tags trigger full releases with 30-day retention
- **Multiple Targets**: Builds for Ubuntu 20.04, 22.04, and 24.04 compatibility  
- **Compressed**: Executables are compressed with UPX for smaller download size
- **Universal Binary**: The main `task-tracker` executable works on most Linux distributions

### Manual Release
```bash
# Create local release package
make release

# Or with specific version
./release.sh v1.2.3
```

### Distribution Requirements
The standalone executable (`task-tracker`) bundles all Python dependencies and can be distributed as a single file. Target systems only need:
- Compatible Linux distribution (x86_64)
- GTK4 system libraries (typically pre-installed)
- wmctrl for always-on-top feature (optional)