import json
from pathlib import Path
import os

class Settings:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'task-tracker'
        self.config_file = self.config_dir / 'settings.json'
        self.settings = {
            'last_file': None,
            'window_width': 400,
            'window_height': 600,
            'window_x': None,
            'window_y': None,
            'always_on_top': False
        }
        self.load()
    
    def load(self):
        """Load settings from config file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Could not load settings: {e}")
    
    def save(self):
        """Save current settings to config file"""
        try:
            # Create config directory if it doesn't exist
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            print(f"Could not save settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value and save"""
        self.settings[key] = value
        self.save()
    
    def get_last_file(self):
        """Get the last opened file path"""
        last_file = self.settings.get('last_file')
        if last_file and Path(last_file).exists():
            return last_file
        return None
    
    def set_last_file(self, file_path):
        """Set the last opened file path"""
        self.set('last_file', str(file_path) if file_path else None)
    
    def get_window_geometry(self):
        """Get window geometry settings"""
        return {
            'width': self.settings.get('window_width', 400),
            'height': self.settings.get('window_height', 600),
            'x': self.settings.get('window_x'),
            'y': self.settings.get('window_y')
        }
    
    def set_window_geometry(self, width, height, x=None, y=None):
        """Set window geometry settings"""
        self.settings.update({
            'window_width': width,
            'window_height': height,
            'window_x': x,
            'window_y': y
        })
        self.save()
    
    def get_always_on_top(self):
        """Get always on top setting"""
        return self.settings.get('always_on_top', False)
    
    def set_always_on_top(self, value):
        """Set always on top setting"""
        self.set('always_on_top', bool(value))