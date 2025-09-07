#!/bin/bash
set -e

# Task Tracker Release Script
# Usage: ./release.sh [version]

VERSION=${1:-"v1.0.0"}
RELEASE_DIR="release-$VERSION"

echo "🚀 Creating Task Tracker release $VERSION"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
make clean

# Build executable
echo "🔨 Building executable..."
make build

# Test executable
echo "🧪 Testing executable..."
./dist/task-tracker --help > /dev/null
echo "✅ Executable test passed"

# Create release directory
echo "📦 Preparing release files..."
mkdir -p "$RELEASE_DIR"

# Copy executable
cp dist/task-tracker "$RELEASE_DIR/"
chmod +x "$RELEASE_DIR/task-tracker"

# Copy documentation
cp README.md "$RELEASE_DIR/"
cp tasks.md "$RELEASE_DIR/sample-tasks.md"

# Create release notes
cat > "$RELEASE_DIR/RELEASE_NOTES.md" << EOF
# Task Tracker $VERSION

A lightweight Linux desktop application for managing markdown task lists with interactive checkboxes.

## Installation

1. Extract this archive
2. Make the executable runnable: \`chmod +x task-tracker\`  
3. Run the application: \`./task-tracker\`

## System Requirements

- Linux x86_64 with GTK4 libraries (usually pre-installed)
- Optional: wmctrl for always-on-top functionality (\`sudo apt install wmctrl\`)

## Features

- Interactive markdown task list management
- Auto-save changes to source files  
- Smart window resizing
- Always-on-top mode
- Modern GTK4 interface
- File persistence and settings

## Usage

1. **First Run**: The app will load \`tasks.md\` from the current directory if it exists
2. **Open Files**: Click the folder icon (📁) to open any markdown file with task lists
3. **Check Tasks**: Click checkboxes to mark tasks complete - changes save automatically
4. **Always on Top**: Click the pin icon (📌) to keep window above other applications
5. **Auto-Resize**: Window automatically adjusts size when loading different files

## Task Format

Your markdown files should contain tasks in this format:
\`\`\`markdown
- [ ] Uncompleted task
- [x] Completed task
\`\`\`

For more information, see README.md
EOF

# Get file sizes
EXECUTABLE_SIZE=$(du -h "$RELEASE_DIR/task-tracker" | cut -f1)

echo "📊 Release Summary:"
echo "   Version: $VERSION"
echo "   Executable size: $EXECUTABLE_SIZE"
echo "   Release directory: $RELEASE_DIR/"
echo ""
echo "📋 Files in release:"
ls -la "$RELEASE_DIR/"

echo ""
echo "✅ Release $VERSION ready in $RELEASE_DIR/"
echo ""
echo "To create a GitHub release:"
echo "1. Create and push a git tag: git tag $VERSION && git push origin $VERSION"
echo "2. The GitHub Actions workflow will automatically create the release"
echo ""
echo "To test locally:"
echo "   cd $RELEASE_DIR && ./task-tracker"