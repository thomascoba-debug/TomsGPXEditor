import tkinter as tk
from tkinter import ttk

# Test logging settings dialog directly
print("Testing logging settings dialog...")

# Create a simple properties class
class TestProperties:
    def __init__(self):
        self.data = {
            "session_files": {
                "1": {"path": "test.gpx", "settings": {"color": "#ff0000"}}
            },
            "log_level": "INFO",
            "log_file": "test.log"
        }
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value
        print(f"Set {key} = {value}")

# Create test app
root = tk.Tk()
root.title("Logging Test")

# Create properties instance
props = TestProperties()

print(f"Initial log_level: {props.get('log_level')}")
print(f"Initial log_file: {props.get('log_file')}")

# Simulate logging dialog
level_var = tk.StringVar(value=props.get("log_level"))
logfile_var = tk.StringVar(value=props.get("log_file"))

# Test changing values
print("\nChanging log level to WARNING...")
level_var.set("WARNING")
props.set("log_level", "WARNING")

print("Changing log file to warning_test.log...")
logfile_var.set("warning_test.log")
props.set("log_file", "warning_test.log")

print(f"After changes - log_level: {props.get('log_level')}")
print(f"After changes - log_file: {props.get('log_file')}")

# Simulate save callback (like dialog OK button)
def save_callback():
    print("Save callback called!")
    print(f"Final log_level: {props.get('log_level')}")
    print(f"Final log_file: {props.get('log_file')}")

# Create dialog interface
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(frame, text="Log Level").grid(row=0, column=0, sticky="w")
level_box = ttk.Combobox(frame, textvariable=level_var, values=["DEBUG", "INFO", "WARNING", "ERROR"])
level_box.grid(row=0, column=1, sticky="ew")

ttk.Label(frame, text="Log File").grid(row=1, column=0, sticky="w")
entry = ttk.Entry(frame, textvariable=logfile_var, width=40)
entry.grid(row=1, column=1, sticky="ew")

ttk.Button(frame, text="OK", command=save_callback).grid(row=2, column=0, columnspan=2, pady=10)

print("Dialog created. Testing...")

root.mainloop()
