#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GdkX11', '4.0')
gi.require_version('Gio', '2.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, GLib, GdkX11, Gio, Gdk
import sys
import subprocess
from pathlib import Path
from task_parser import TaskParser, Task
from settings import Settings

class TaskTrackerWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Task Tracker")
        
        self.parser = TaskParser()
        self.task_checkboxes = []
        self.settings = Settings()
        
        # Set up window with saved geometry
        geometry = self.settings.get_window_geometry()
        self.set_default_size(geometry['width'], geometry['height'])
        self.set_resizable(True)
        
        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        self.set_child(main_box)
        
        # Create toolbar
        toolbar = self.create_toolbar()
        main_box.append(toolbar)
        
        # Create scrolled window for tasks
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        
        # Create task list container
        self.task_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        scrolled.set_child(self.task_list)
        
        main_box.append(scrolled)
        
        # Load last opened file or default file
        last_file = self.settings.get_last_file()
        if last_file:
            self.load_file(last_file)
        else:
            # Fallback to default file if exists
            default_file = Path.cwd() / "tasks.md"
            if default_file.exists():
                self.load_file(str(default_file))
    
    def create_toolbar(self):
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Open file button with folder icon
        open_button = Gtk.Button()
        open_icon = Gtk.Image.new_from_icon_name("folder-open-symbolic")
        open_button.set_child(open_icon)
        open_button.set_tooltip_text("Open File")
        open_button.connect("clicked", self.on_open_file)
        toolbar.append(open_button)
        
        # Always on top toggle with pin icon
        self.always_on_top_button = Gtk.ToggleButton()
        self.pin_icon = Gtk.Image.new_from_icon_name("view-pin-symbolic")
        self.always_on_top_button.set_child(self.pin_icon)
        self.always_on_top_button.set_tooltip_text("Always on Top")
        self.always_on_top_button.set_active(self.settings.get_always_on_top())
        self.always_on_top_button.connect("toggled", self.on_always_on_top_toggled)
        toolbar.append(self.always_on_top_button)
        
        # File label
        self.file_label = Gtk.Label(label="No file loaded")
        self.file_label.set_ellipsize(3)  # ELLIPSIZE_END
        self.file_label.set_hexpand(True)
        self.file_label.set_xalign(1.0)
        toolbar.append(self.file_label)
        
        return toolbar
    
    def on_open_file(self, button):
        dialog = Gtk.FileDialog(title="Open Markdown File")
        
        # Create file filter for markdown files
        filter_md = Gtk.FileFilter()
        filter_md.set_name("Markdown files")
        filter_md.add_pattern("*.md")
        filter_md.add_pattern("*.markdown")
        
        # Create filter list
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(filter_md)
        
        # Set filters on dialog
        dialog.set_filters(filters)
        dialog.set_default_filter(filter_md)
        
        # Open dialog asynchronously
        dialog.open(self, None, self.on_file_dialog_response)
    
    def on_file_dialog_response(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file:
                file_path = file.get_path()
                self.load_file(file_path)
        except GLib.Error as error:
            print(f"File dialog cancelled or error: {error.message}")
    
    def on_always_on_top_toggled(self, button):
        """Toggle always on top using wmctrl"""
        # Save the setting
        self.settings.set_always_on_top(button.get_active())
        
        try:
            # Get window XID
            surface = self.get_surface()
            if not surface:
                print("No surface available")
                return
                
            if isinstance(surface, GdkX11.X11Surface):
                xid = GdkX11.X11Surface.get_xid(surface)
                xid_hex = hex(xid)
                
                if button.get_active():
                    # Add always on top state
                    subprocess.run([
                        'wmctrl', '-i', '-r', xid_hex, '-b', 'add,above'
                    ], check=True)
                    print(f"Set window {xid_hex} always on top")
                else:
                    # Remove always on top state
                    subprocess.run([
                        'wmctrl', '-i', '-r', xid_hex, '-b', 'remove,above'
                    ], check=True)
                    print(f"Removed always on top for window {xid_hex}")
            else:
                print("Not running on X11, always on top not supported")
                
        except subprocess.CalledProcessError as e:
            print(f"wmctrl command failed: {e}")
            print("Install wmctrl: sudo apt install wmctrl")
        except Exception as e:
            print(f"Could not set always on top: {e}")
            print("This feature requires X11 and wmctrl")
    
    def load_file(self, file_path: str):
        if self.parser.load_file(file_path):
            self.file_label.set_text(Path(file_path).name)
            self.settings.set_last_file(file_path)
            self.refresh_task_list()
            # Resize window to fit content
            GLib.idle_add(self.resize_to_fit_content)
        else:
            self.show_error_dialog("Failed to load file", f"Could not load: {file_path}")
    
    def refresh_task_list(self):
        # Clear existing widgets
        while self.task_list.get_first_child():
            self.task_list.remove(self.task_list.get_first_child())
        
        self.task_checkboxes.clear()
        
        # Add task checkboxes
        for i, task in enumerate(self.parser.get_tasks()):
            task_row = self.create_task_row(task, i)
            self.task_list.append(task_row)
    
    def create_task_row(self, task: Task, index: int):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.set_margin_start(5)
        row.set_margin_end(5)
        
        # Checkbox
        checkbox = Gtk.CheckButton()
        checkbox.set_active(task.completed)
        checkbox.connect("toggled", self.on_task_toggled, index)
        self.task_checkboxes.append(checkbox)
        
        # Task text
        label = Gtk.Label(label=task.text)
        label.set_xalign(0.0)
        label.set_hexpand(True)
        label.set_wrap(True)
        
        # Apply strikethrough style if completed
        if task.completed:
            label.add_css_class("strikethrough")
        
        row.append(checkbox)
        row.append(label)
        
        return row
    
    def on_task_toggled(self, checkbox, task_index):
        completed = checkbox.get_active()
        if self.parser.update_task_status(task_index, completed):
            # Update label styling
            row = checkbox.get_parent()
            label = row.get_last_child()
            
            if completed:
                label.add_css_class("strikethrough")
            else:
                label.remove_css_class("strikethrough")
    
    def resize_to_fit_content(self):
        """Resize window to fit task content with screen bounds constraints"""
        try:
            # Get screen dimensions
            display = self.get_display()
            if not display:
                return False
            
            monitor = display.get_monitors().get_item(0)  # Primary monitor
            if not monitor:
                return False
            
            geometry = monitor.get_geometry()
            screen_width = geometry.width
            screen_height = geometry.height
            
            # Calculate content size
            num_tasks = len(self.parser.get_tasks())
            
            # Base window size (toolbar + margins + padding)
            base_height = 45   # Toolbar + margins (minimal)
            base_width = 300   # Minimum useful width
            
            # Calculate height based on tasks (precise fit)
            task_height = 22   # Height per task row (tight fit)
            spacing = 5        # Spacing between tasks
            content_height = base_height + (num_tasks * task_height) + ((num_tasks - 1) * spacing) if num_tasks > 0 else base_height
            
            # Calculate width based on longest task text
            max_task_width = 0
            for task in self.parser.get_tasks():
                # Rough character width estimation (8 pixels per char)
                task_width = len(task.text) * 8 + 60  # 60px for checkbox + margins
                max_task_width = max(max_task_width, task_width)
            
            content_width = max(base_width, max_task_width)
            
            # Apply screen bounds constraints (leave 10% margin on each side)
            max_width = int(screen_width * 0.8)
            max_height = int(screen_height * 0.8)
            
            # Constrain dimensions
            new_width = max(300, min(content_width, max_width))
            new_height = max(200, min(content_height, max_height))
            
            # Set new size
            self.set_default_size(new_width, new_height)
            
            # Save the new geometry
            self.settings.set_window_geometry(new_width, new_height)
            
            print(f"Resized window to {new_width}x{new_height} for {num_tasks} tasks")
            
        except Exception as e:
            print(f"Error resizing window: {e}")
        
        return False  # Don't repeat this idle callback
    
    def show_error_dialog(self, title: str, message: str):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title
        )
        dialog.format_secondary_text(message)
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.present()

class TaskTrackerApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.tasktracker")
        
    def do_activate(self):
        window = TaskTrackerWindow(self)
        
        # Add CSS for strikethrough
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
        .strikethrough {
            text-decoration: line-through;
            opacity: 0.7;
        }
        """)
        
        Gtk.StyleContext.add_provider_for_display(
            window.get_display(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        window.present()

def main():
    app = TaskTrackerApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    main()