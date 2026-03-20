from pathlib import Path

base_dir = Path(__file__).parent

# 1. Create nested directories
nested_dir = base_dir / "workspace" / "projects" / "python"
nested_dir.mkdir(parents=True, exist_ok=True)
print("Nested directories created:", nested_dir)

# 2. List files and folders
print("\nFiles and folders in current directory:")
for item in base_dir.iterdir():
    print(item.name)

# 3. Find files by extension
print("\nPython files:")
for item in base_dir.iterdir():
    if item.is_file() and item.suffix == ".py":
        print(item.name)