import json
import os
import ast

DEFAULT_SCHEMA = {
    "session_files": dict,
    "dialog_geometry": dict,
    "log_level": str,
    "log_file": str,
    "marker_enabled": bool,
    "marker_step": int,
    "marker_icon_size": list,
    "marker_icon_path": str,
    "zoom_scaling_enabled": bool,
    "downsample_step": int
}

def clean_properties(path="properties.json"):
    if not os.path.exists(path):
        print(f"{path} nicht gefunden.")
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Reparatur: Strings, die wie Listen/Dictionaries aussehen, in echte Objekte umwandeln
    for key, value in list(data.items()):
        if isinstance(value, str):
            v = value.strip()
            if (v.startswith("[") and v.endswith("]")) or (v.startswith("{") and v.endswith("}")):
                try:
                    parsed = ast.literal_eval(v)
                    data[key] = parsed
                except Exception:
                    pass
    cleaned = {}
    for key, typ in DEFAULT_SCHEMA.items():
        if key in data:
            value = data[key]
            # Typ prüfen und leere Werte überspringen
            if typ == dict and isinstance(value, dict):
                # file_settings speziell behandeln: nur gültige Einträge behalten
                if key == "file_settings":
                    valid = {}
                    for k, v in value.items():
                        if isinstance(v, dict) and v:
                            valid[k] = v
                    if valid:
                        cleaned[key] = valid
                elif value:
                    cleaned[key] = value
            elif typ == list and isinstance(value, list) and value:
                cleaned[key] = value
            elif typ == bool and isinstance(value, bool):
                cleaned[key] = value
            elif typ == int and isinstance(value, int):
                cleaned[key] = value
            elif typ == str and isinstance(value, str) and value:
                cleaned[key] = value
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)
    print(f"{path} wurde bereinigt.")

if __name__ == "__main__":
    clean_properties()
