import logging
from abc import ABC, abstractmethod
from typing import List, Any

logger = logging.getLogger(__name__)


class Command(ABC):
    """Base class for undoable commands"""
    
    @abstractmethod
    def execute(self):
        """Execute the command"""
        pass
    
    @abstractmethod
    def undo(self):
        """Undo the command"""
        pass
    
    @abstractmethod
    def get_description(self):
        """Get a description of the command for UI display"""
        pass


class PointMoveCommand(Command):
    """Command for moving a point in the table"""
    
    def __init__(self, table_editor, from_index, to_index, point_data):
        self.table_editor = table_editor
        self.from_index = from_index
        self.to_index = to_index
        self.point_data = point_data
        self.original_from_index = from_index
        self.original_to_index = to_index
    
    def execute(self):
        """Move the point from from_index to to_index"""
        try:
            # Remove point from original position
            point = self.table_editor.working_document.gpx.tracks[0].segments[0].points.pop(self.from_index)
            
            # Insert at new position
            self.table_editor.working_document.gpx.tracks[0].segments[0].points.insert(self.to_index, point)
            
            # Update indices if needed
            if self.from_index < self.to_index:
                self.from_index = self.to_index - 1
            else:
                self.from_index = self.to_index + 1
            
            logger.debug(f"Moved point from index {self.original_from_index} to {self.to_index}")
            return True
        except Exception as e:
            logger.error(f"Failed to execute point move: {e}")
            return False
    
    def undo(self):
        """Undo the point move"""
        try:
            # Remove point from current position
            point = self.table_editor.working_document.gpx.tracks[0].segments[0].points.pop(self.to_index)
            
            # Insert back at original position
            self.table_editor.working_document.gpx.tracks[0].segments[0].points.insert(self.original_from_index, point)
            
            logger.debug(f"Undid point move from {self.original_from_index} to {self.to_index}")
            return True
        except Exception as e:
            logger.error(f"Failed to undo point move: {e}")
            return False
    
    def get_description(self):
        return f"Move point from position {self.original_from_index + 1} to {self.to_index + 1}"


class PointEditCommand(Command):
    """Command for editing point data"""
    
    def __init__(self, table_editor, index, field, old_value, new_value):
        self.table_editor = table_editor
        self.index = index
        self.field = field
        self.old_value = old_value
        self.new_value = new_value
    
    def execute(self):
        """Apply the edit"""
        try:
            point = self.table_editor.working_document.gpx.tracks[0].segments[0].points[self.index]
            
            if self.field == 'lat':
                point.latitude = float(self.new_value)
            elif self.field == 'lon':
                point.longitude = float(self.new_value)
            elif self.field == 'ele':
                point.elevation = float(self.new_value) if self.new_value else None
            elif self.field == 'time':
                # Time parsing would go here
                pass
            
            logger.debug(f"Edited point {self.index} {self.field}: {self.old_value} -> {self.new_value}")
            return True
        except Exception as e:
            logger.error(f"Failed to execute point edit: {e}")
            return False
    
    def undo(self):
        """Undo the edit"""
        try:
            point = self.table_editor.working_document.gpx.tracks[0].segments[0].points[self.index]
            
            if self.field == 'lat':
                point.latitude = float(self.old_value)
            elif self.field == 'lon':
                point.longitude = float(self.old_value)
            elif self.field == 'ele':
                point.elevation = float(self.old_value) if self.old_value else None
            elif self.field == 'time':
                # Time parsing would go here
                pass
            
            logger.debug(f"Undid point {self.index} {self.field}: {self.new_value} -> {self.old_value}")
            return True
        except Exception as e:
            logger.error(f"Failed to undo point edit: {e}")
            return False
    
    def get_description(self):
        return f"Edit point {self.index + 1} {self.field}"


class CommandManager:
    """Manages undo/redo functionality"""
    
    def __init__(self):
        self.history: List[Command] = []
        self.current_index = -1
        self.max_history = 100  # Limit history size
    
    def execute_command(self, command: Command):
        """Execute a command and add to history"""
        if command.execute():
            # Remove any commands after current position
            self.history = self.history[:self.current_index + 1]
            
            # Add new command
            self.history.append(command)
            
            # Limit history size
            if len(self.history) > self.max_history:
                self.history.pop(0)
            else:
                self.current_index += 1
            
            logger.debug(f"Executed command: {command.get_description()}")
            return True
        return False
    
    def undo(self):
        """Undo the last command"""
        if self.can_undo():
            command = self.history[self.current_index]
            if command.undo():
                self.current_index -= 1
                logger.debug(f"Undid command: {command.get_description()}")
                return True
        return False
    
    def redo(self):
        """Redo the next command"""
        if self.can_redo():
            self.current_index += 1
            command = self.history[self.current_index]
            if command.execute():
                logger.debug(f"Redid command: {command.get_description()}")
                return True
            else:
                self.current_index -= 1  # Rollback on failure
                return False
        return False
    
    def can_undo(self):
        """Check if undo is possible"""
        return self.current_index >= 0
    
    def can_redo(self):
        """Check if redo is possible"""
        return self.current_index < len(self.history) - 1
    
    def get_undo_description(self):
        """Get description of command to undo"""
        if self.can_undo():
            return f"Undo: {self.history[self.current_index].get_description()}"
        return "Nothing to undo"
    
    def get_redo_description(self):
        """Get description of command to redo"""
        if self.can_redo():
            return f"Redo: {self.history[self.current_index + 1].get_description()}"
        return "Nothing to redo"
    
    def clear_history(self):
        """Clear the command history"""
        self.history.clear()
        self.current_index = -1
        logger.debug("Command history cleared")
