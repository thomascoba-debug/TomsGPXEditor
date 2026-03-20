import json
import os

# Test save mechanism directly
print("Testing save mechanism...")

# Load current properties
with open("properties.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Current log_level: {data.get('log_level')}")
print(f"Current log_file: {data.get('log_file')}")

# Test save mechanism
class TestProps:
    def __init__(self):
        self.data = data
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value
        print(f"Set {key} = {value}")
    
    def save(self):
        with open("properties.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print(f"Saved properties to JSON")

# Test
props = TestProps()

# Change values
print("\nChanging values...")
props.set("log_level", "TEST_NEW_LEVEL")
props.set("log_file", "test_save_mechanism.log")

# Save
print("\nSaving...")
props.save()

# Reload and verify
print("\nReloading...")
with open("properties.json", "r", encoding="utf-8") as f:
    reloaded = json.load(f)

print(f"After reload - log_level: {reloaded.get('log_level')}")
print(f"After reload - log_file: {reloaded.get('log_file')}")
