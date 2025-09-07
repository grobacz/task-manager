.PHONY: install run clean help build release

# Default target
help:
	@echo "Available targets:"
	@echo "  install  - Install all dependencies (Python packages and wmctrl)"
	@echo "  run      - Run the task tracker application"
	@echo "  build    - Create standalone executable"
	@echo "  release  - Create local release package"
	@echo "  clean    - Clean Python cache files and build artifacts"
	@echo "  help     - Show this help message"

# Install all dependencies
install:
	@echo "Installing system dependencies..."
	sudo apt update
	sudo apt install -y wmctrl python3-pip python3-dev python3-gi python3-gi-cairo gir1.2-gtk-4.0
	@echo "Installing Python requirements..."
	pip3 install --user -r requirements.txt
	@echo "Setup complete! Run 'make run' to start the application."

# Run the application
run:
	@cd src && python3 main.py

# Build standalone executable
build:
	@echo "Building standalone executable..."
	python3 build.py

# Create local release package
release:
	@echo "Creating local release package..."
	./release.sh

# Clean Python cache and build artifacts
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf dist/ build/ *.spec .build-venv/ release-v*/ 2>/dev/null || true

# Install just Python dependencies (no sudo required)
install-python:
	@echo "Installing Python requirements..."
	pip3 install --user -r requirements.txt