from app import TomsGPXEditor
from basic_single_instance import check_single_instance_with_force
from src.i18n.language_manager import initialize_language_manager
from src.infrastructure.repositories.properties_repository import AppProperties


def main():
    # Check for single instance with force option
    if not check_single_instance_with_force():
        return
    
    try:
        # Initialize global language manager FIRST
        properties = AppProperties()
        initialize_language_manager(properties)
        
        app = TomsGPXEditor()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        # Force cleanup on crash
        from basic_single_instance import BasicSingleInstance
        manager = BasicSingleInstance()
        manager.release()


if __name__ == "__main__":
    main()
