#!/bin/bash

# CI-specific build wrapper script
# Ensures proper Python environment for GitHub Actions

set -e

echo "🔧 Setting up CI build environment..."

# Set Python path to include system packages
export PYTHONPATH="/usr/lib/python3/dist-packages:/usr/lib/python3.12/dist-packages:$PYTHONPATH"

# Verify environment
echo "Python version: $(python3 --version)"
echo "Python path: $(which python3)"
echo "PYTHONPATH: $PYTHONPATH"

# Test GTK4 availability
echo "Testing GTK4 imports..."
python3 -c "
import gi
print('✅ gi imported from:', gi.__file__)
gi.require_version('Gtk', '4.0')  
from gi.repository import Gtk
print('✅ GTK4 imported successfully')
"

# Run the build
echo "🚀 Starting build process..."
python3 build.py

echo "✅ CI build completed successfully!"