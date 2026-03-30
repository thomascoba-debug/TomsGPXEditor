#!/usr/bin/env python3
"""
Safe Dead Code Cleanup Script

This script removes identified unused functions and classes.
REVIEW THE CHANGES BEFORE APPLYING!
"""

import os
import shutil

def backup_file(file_path):
    """Create backup of file before modification"""
    backup_path = file_path + '.dead_code_backup'
    shutil.copy2(file_path, backup_path)
    print(f"Backed up: {backup_path}")

def remove_unused_function(file_path, function_name):
    """Remove a specific function from a file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and remove the function
    lines = content.split('\n')
    in_function = False
    function_indent = 0
    start_line = -1
    end_line = -1
    
    for i, line in enumerate(lines):
        if f'def {function_name}(' in line:
            start_line = i
            in_function = True
            function_indent = len(line) - len(line.lstrip())
        elif in_function:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= function_indent:
                end_line = i - 1
                break
    
    if start_line >= 0:
        # Remove the function
        new_lines = lines[:start_line] + lines[end_line + 1:]
        with open(file_path, 'w') as f:
            f.write('\n'.join(new_lines))
        print(f"Removed function {function_name} from {os.path.basename(file_path)}")
        return True
    
    return False

def remove_unused_class(file_path, class_name):
    """Remove a specific class from a file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and remove the class
    lines = content.split('\n')
    in_class = False
    class_indent = 0
    start_line = -1
    end_line = -1
    
    for i, line in enumerate(lines):
        if f'class {class_name}' in line:
            start_line = i
            in_class = True
            class_indent = len(line) - len(line.lstrip())
        elif in_class:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= class_indent:
                end_line = i - 1
                break
    
    if start_line >= 0:
        # Remove the class
        new_lines = lines[:start_line] + lines[end_line + 1:]
        with open(file_path, 'w') as f:
            f.write('\n'.join(new_lines))
        print(f"Removed class {class_name} from {os.path.basename(file_path)}")
        return True
    
    return False

def main():
    """Main cleanup function"""
    print("Starting safe dead code cleanup...")
    
    # Unused functions to remove (REVIEW THESE!)
    unused_functions = [{'name': 'clear_all_entries', 'file': 'W:/TomsGPXEditor/src\\application\\gpx_file_manager.py', 'type': 'function'}, {'name': 'failing_handler', 'file': 'W:/TomsGPXEditor/src\\application\\test_event_bus.py', 'type': 'function'}, {'name': 'working_handler', 'file': 'W:/TomsGPXEditor/src\\application\\test_event_bus.py', 'type': 'function'}, {'name': 'clear_history', 'file': 'W:/TomsGPXEditor/src\\application\\services\\command_service.py', 'type': 'function'}, {'name': 'analyze_gpx_file', 'file': 'W:/TomsGPXEditor/src\\application\\services\\gpx_service.py', 'type': 'function'}, {'name': 'clear_recent_files', 'file': 'W:/TomsGPXEditor/src\\application\\services\\recent_files_service.py', 'type': 'function'}, {'name': 'sync_with_session_files', 'file': 'W:/TomsGPXEditor/src\\application\\services\\recent_files_service.py', 'type': 'function'}, {'name': 'build_app_path', 'file': 'W:/TomsGPXEditor/src\\constants\\property_keys.py', 'type': 'function'}, {'name': 'build_dialogs_path', 'file': 'W:/TomsGPXEditor/src\\constants\\property_keys.py', 'type': 'function'}, {'name': 'build_rendering_path', 'file': 'W:/TomsGPXEditor/src\\constants\\property_keys.py', 'type': 'function'}, {'name': 'build_logging_path', 'file': 'W:/TomsGPXEditor/src\\constants\\property_keys.py', 'type': 'function'}, {'name': 'handle_file_error', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\error_handler.py', 'type': 'function'}, {'name': 'decorator', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\shutdown_manager.py', 'type': 'function'}, {'name': 'wrapper', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\shutdown_manager.py', 'type': 'function'}, {'name': 'clear_cache', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\map_renderer_optimized.py', 'type': 'function'}, {'name': 'enable_validation', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\properties_manager.py', 'type': 'function'}, {'name': 'force_validation', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\properties_manager.py', 'type': 'function'}, {'name': 'data', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\properties_manager.py', 'type': 'function'}, {'name': 'register_resource', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\resource_manager.py', 'type': 'function'}, {'name': 'cleanup_all', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\resource_manager.py', 'type': 'function'}, {'name': 'managed_file', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\resource_manager.py', 'type': 'function'}, {'name': 'managed_temp_file', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\resource_manager.py', 'type': 'function'}, {'name': 'shutdown_handler', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\shutdown_manager.py', 'type': 'function'}, {'name': 'is_shutting_down', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\state_manager.py', 'type': 'function'}, {'name': 'signal_handler', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\shutdown_manager.py', 'type': 'function'}, {'name': 'state', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\state_manager.py', 'type': 'function'}, {'name': 'register_state_change_callback', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\state_manager.py', 'type': 'function'}, {'name': 'unregister_state_change_callback', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\state_manager.py', 'type': 'function'}, {'name': 'is_ready', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\state_manager.py', 'type': 'function'}, {'name': 'browse', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_logging_dialog.py', 'type': 'function'}, {'name': 'on_lines_change', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_logging_dialog.py', 'type': 'function'}, {'name': 'start_resize', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_logging_dialog.py', 'type': 'function'}, {'name': 'on_resize', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_logging_dialog.py', 'type': 'function'}, {'name': 'stop_resize', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_logging_dialog.py', 'type': 'function'}, {'name': 'clear_log_file', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_logging_dialog.py', 'type': 'function'}, {'name': 'ok', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_rendering_dialog.py', 'type': 'function'}, {'name': 'cancel', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\progress_dialog.py', 'type': 'function'}, {'name': 'validate_percent_input', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_marker_dialog.py', 'type': 'function'}, {'name': 'validate_percent_keypress', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_marker_dialog.py', 'type': 'function'}, {'name': 'on_enter', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_marker_dialog.py', 'type': 'function'}, {'name': 'on_leave', 'file': 'W:/TomsGPXEditor/src\\ui\\dialogs\\settings_marker_dialog.py', 'type': 'function'}, {'name': 'unregister_shortcut', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\context_menu.py', 'type': 'function'}, {'name': 'clear_search', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\file_search.py', 'type': 'function'}, {'name': 'search_files', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\file_search.py', 'type': 'function'}, {'name': 'highlight_search_term', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\file_search.py', 'type': 'function'}, {'name': 'on_page_size_changed', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\pagination_manager.py', 'type': 'function'}, {'name': 'close_editor', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\gpx_table_editor.py', 'type': 'function'}, {'name': 'run_with_progress', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\progress_dialog.py', 'type': 'function'}, {'name': 'close_dialog', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\progress_dialog.py', 'type': 'function'}, {'name': 'worker', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\progress_dialog.py', 'type': 'function'}]
    
    # Unused classes to remove (REVIEW THESE!)
    unused_classes = [{'name': 'DialogController', 'file': 'W:/TomsGPXEditor/src\\application\\dialog_controller.py', 'type': 'class'}, {'name': 'FileVisibleChangedEvent', 'file': 'W:/TomsGPXEditor/src\\application\\event_bus.py', 'type': 'class'}, {'name': 'FileColorChangedEvent', 'file': 'W:/TomsGPXEditor/src\\application\\event_bus.py', 'type': 'class'}, {'name': 'ConversionCompletedEvent', 'file': 'W:/TomsGPXEditor/src\\application\\event_bus.py', 'type': 'class'}, {'name': 'GPXFileManager', 'file': 'W:/TomsGPXEditor/src\\application\\gpx_file_manager.py', 'type': 'class'}, {'name': 'MapController', 'file': 'W:/TomsGPXEditor/src\\application\\map_controller.py', 'type': 'class'}, {'name': 'TestEventBus', 'file': 'W:/TomsGPXEditor/src\\application\\test_event_bus.py', 'type': 'class'}, {'name': 'TestGlobalEventBus', 'file': 'W:/TomsGPXEditor/src\\application\\test_event_bus.py', 'type': 'class'}, {'name': 'TestEventTypes', 'file': 'W:/TomsGPXEditor/src\\application\\test_event_bus.py', 'type': 'class'}, {'name': 'Command', 'file': 'W:/TomsGPXEditor/src\\application\\services\\command_service.py', 'type': 'class'}, {'name': 'AppCore', 'file': 'W:/TomsGPXEditor/src\\core\\app_core.py', 'type': 'class'}, {'name': 'TestGPXFile', 'file': 'W:/TomsGPXEditor/src\\domain\\entities\\test_gpx_entities.py', 'type': 'class'}, {'name': 'TestGPXTrack', 'file': 'W:/TomsGPXEditor/src\\domain\\entities\\test_gpx_entities.py', 'type': 'class'}, {'name': 'TestGPXTrackSegment', 'file': 'W:/TomsGPXEditor/src\\domain\\entities\\test_gpx_entities.py', 'type': 'class'}, {'name': 'TestGPXRoute', 'file': 'W:/TomsGPXEditor/src\\domain\\entities\\test_gpx_entities.py', 'type': 'class'}, {'name': 'PropertiesManager', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\properties_manager.py', 'type': 'class'}, {'name': 'ResourceManager', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\resource_manager.py', 'type': 'class'}, {'name': 'ShutdownPriority', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\shutdown_manager.py', 'type': 'class'}, {'name': 'ShutdownManager', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\shutdown_manager.py', 'type': 'class'}, {'name': 'StabilityManager', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\stability_manager.py', 'type': 'class'}, {'name': 'ApplicationState', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\state_manager.py', 'type': 'class'}, {'name': 'StateManager', 'file': 'W:/TomsGPXEditor/src\\infrastructure\\state_manager.py', 'type': 'class'}, {'name': 'SimpleEntry', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\file_entry_builder.py', 'type': 'class'}, {'name': 'PaginationManager', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\pagination_manager.py', 'type': 'class'}, {'name': 'ProgressDialog', 'file': 'W:/TomsGPXEditor/src\\ui\\widgets\\progress_dialog.py', 'type': 'class'}]
    
    print("WARNING: This will remove unused code. Review the lists above carefully!")
    print("Press Ctrl+C to cancel, or press Enter to continue...")
    input()
    
    # Remove unused functions
    for func in unused_functions:
        if os.path.exists(func['file']):
            backup_file(func['file'])
            remove_unused_function(func['file'], func['name'])
    
    # Remove unused classes
    for cls in unused_classes:
        if os.path.exists(cls['file']):
            backup_file(cls['file'])
            remove_unused_class(cls['file'], cls['name'])
    
    print("Dead code cleanup complete!")

if __name__ == "__main__":
    main()
