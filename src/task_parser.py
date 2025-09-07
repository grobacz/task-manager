import re
from pathlib import Path
from typing import List, Tuple, Optional

class Task:
    def __init__(self, text: str, completed: bool, line_number: int, indent: str = ""):
        self.text = text
        self.completed = completed
        self.line_number = line_number
        self.indent = indent

class TaskParser:
    TASK_PATTERN = re.compile(r'^(\s*)-\s\[([ x])\]\s(.+)$')
    
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = Path(file_path) if file_path else None
        self.tasks: List[Task] = []
        self.file_lines: List[str] = []
    
    def load_file(self, file_path: str) -> bool:
        """Load tasks from markdown file"""
        try:
            self.file_path = Path(file_path)
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.file_lines = f.readlines()
            
            self._parse_tasks()
            return True
        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
            print(f"Error loading file: {e}")
            return False
    
    def _parse_tasks(self):
        """Parse tasks from loaded file lines"""
        self.tasks.clear()
        
        for line_num, line in enumerate(self.file_lines):
            line = line.rstrip('\n')
            match = self.TASK_PATTERN.match(line)
            
            if match:
                indent = match.group(1)
                status = match.group(2)
                text = match.group(3)
                completed = status.lower() == 'x'
                
                task = Task(text, completed, line_num, indent)
                self.tasks.append(task)
    
    def get_tasks(self) -> List[Task]:
        """Get list of parsed tasks"""
        return self.tasks
    
    def update_task_status(self, task_index: int, completed: bool) -> bool:
        """Update task completion status and save to file"""
        if not (0 <= task_index < len(self.tasks)):
            return False
        
        task = self.tasks[task_index]
        task.completed = completed
        
        # Update the corresponding line in file_lines
        new_status = 'x' if completed else ' '
        new_line = f"{task.indent}- [{new_status}] {task.text}\n"
        
        if task.line_number < len(self.file_lines):
            self.file_lines[task.line_number] = new_line
            return self._save_file()
        
        return False
    
    def _save_file(self) -> bool:
        """Save current file_lines back to file"""
        if not self.file_path:
            return False
        
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.writelines(self.file_lines)
            return True
        except (PermissionError, IOError) as e:
            print(f"Error saving file: {e}")
            return False
    
    def reload(self) -> bool:
        """Reload tasks from file"""
        if self.file_path and self.file_path.exists():
            return self.load_file(str(self.file_path))
        return False