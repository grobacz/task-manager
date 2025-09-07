#!/usr/bin/env python3
"""
Build script for creating standalone Task Tracker executable
"""

import subprocess
import sys
import os
import venv
from pathlib import Path

def setup_venv(venv_path):
    """Create and setup virtual environment with system site packages"""
    print(f"Creating virtual environment at {venv_path}...")
    
    # Create venv if it doesn't exist, with system site packages for GTK4/PyGObject
    if not venv_path.exists():
        venv.create(venv_path, with_pip=True, system_site_packages=True)
    
    # Get python and pip paths in venv
    if sys.platform == 'win32':
        python_exe = venv_path / 'Scripts' / 'python.exe'
        pip_exe = venv_path / 'Scripts' / 'pip.exe'
    else:
        python_exe = venv_path / 'bin' / 'python'
        pip_exe = venv_path / 'bin' / 'pip'
    
    return python_exe, pip_exe

def main():
    print("Building Task Tracker standalone executable...")
    
    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Setup virtual environment
    venv_path = project_root / '.build-venv'
    python_exe, pip_exe = setup_venv(venv_path)
    
    # Check if system has required packages
    print("Checking system dependencies...")
    try:
        subprocess.check_call([str(python_exe), '-c', 'import gi; gi.require_version("Gtk", "4.0"); from gi.repository import Gtk'])
        print("✅ GTK4 system packages found")
    except subprocess.CalledProcessError:
        print("❌ GTK4 system packages not found. Please install python3-gi and gir1.2-gtk-4.0")
        print("Run: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0")
        return 1
    
    # Install only PyInstaller in venv (PyGObject comes from system)
    print("Installing PyInstaller...")
    subprocess.check_call([str(pip_exe), 'install', 'pyinstaller>=5.0.0', 'watchdog>=3.0.0'])
    
    # Get PyInstaller path in venv
    if sys.platform == 'win32':
        pyinstaller_exe = venv_path / 'Scripts' / 'pyinstaller.exe'
    else:
        pyinstaller_exe = venv_path / 'bin' / 'pyinstaller'
    
    # Build command (simple approach - let PyInstaller auto-detect dependencies)
    build_cmd = [
        str(pyinstaller_exe),
        "--onefile",                    # Single executable file
        "--name=task-tracker",          # Executable name
        "src/main.py"
    ]
    
    try:
        print("Running PyInstaller...")
        print(" ".join(build_cmd))
        subprocess.check_call(build_cmd)
        
        print("\n✅ Build completed successfully!")
        print(f"Executable created: {project_root}/dist/task-tracker")
        print("\nTo test the executable:")
        print("  ./dist/task-tracker")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())