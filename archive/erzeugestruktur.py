import os
from pathlib import Path
from datetime import datetime

# ==============================
# CONFIG
# ==============================

INCLUDE_EXTENSIONS = {".py", ".json", ".txt", ".md", ".ini"}
EXCLUDE_DIRS = {"venv", "__pycache__", ".git", ".idea", "build", "dist"}

PROJECT_ROOT = Path(__file__).parent.resolve()

STRUCTURE_FILE = PROJECT_ROOT / "PROJECT_STRUCTURE.txt"
SOURCE_DUMP_FILE = PROJECT_ROOT / "FULL_SOURCE_DUMP.txt"


# ==============================
# HELPERS
# ==============================

def should_include(file_path: Path) -> bool:
    if file_path.suffix.lower() in INCLUDE_EXTENSIONS:
        return True
    return False


def is_excluded_dir(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


# ==============================
# 1. PROJECT STRUCTURE EXPORT
# ==============================

def export_structure():
    lines = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        root_path = Path(root)

        # Skip excluded dirs
        if is_excluded_dir(root_path):
            continue

        level = len(root_path.relative_to(PROJECT_ROOT).parts)
        indent = "    " * level

        lines.append(f"{indent}{root_path.name}/")

        for file in sorted(files):
            file_path = root_path / file
            if should_include(file_path):
                lines.append(f"{indent}    {file}")

    STRUCTURE_FILE.write_text("\n".join(lines), encoding="utf-8")


# ==============================
# 2. FULL SOURCE DUMP EXPORT
# ==============================

def export_full_source():
    output_lines = []
    header = (
        f"FULL PROJECT EXPORT\n"
        f"Project Root: {PROJECT_ROOT}\n"
        f"Exported: {datetime.now()}\n"
        f"{'='*80}\n\n"
    )

    output_lines.append(header)

    for root, dirs, files in os.walk(PROJECT_ROOT):
        root_path = Path(root)

        if is_excluded_dir(root_path):
            continue

        for file in sorted(files):
            file_path = root_path / file

            if not should_include(file_path):
                continue

            relative_path = file_path.relative_to(PROJECT_ROOT)

            separator = (
                f"\n{'='*80}\n"
                f"FILE: {relative_path}\n"
                f"{'='*80}\n\n"
            )

            output_lines.append(separator)

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception as e:
                content = f"[ERROR READING FILE: {e}]"

            output_lines.append(content)
            output_lines.append("\n")

    SOURCE_DUMP_FILE.write_text("".join(output_lines), encoding="utf-8")


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    print("Exporting project structure...")
    export_structure()

    print("Exporting full source dump...")
    export_full_source()

    print("\nDone.")
    print(f"Structure file: {STRUCTURE_FILE}")
    print(f"Source dump:    {SOURCE_DUMP_FILE}")