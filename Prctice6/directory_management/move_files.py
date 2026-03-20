from pathlib import Path
import shutil

base_dir = Path(__file__).parent
source_dir = base_dir / "source_files"
target_dir = base_dir / "target_files"

source_dir.mkdir(exist_ok=True)
target_dir.mkdir(exist_ok=True)

# Create sample files
file1 = source_dir / "notes.txt"
file2 = source_dir / "program.py"
file3 = source_dir / "data.txt"

for file_path in [file1, file2, file3]:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Sample content for {file_path.name}")

print("Sample files created.")

# Find files by extension
print("\nTXT files in source_files:")
for item in source_dir.iterdir():
    if item.is_file() and item.suffix == ".txt":
        print(item.name)

# Copy one file
shutil.copy(file1, target_dir / file1.name)
print(f"\nCopied {file1.name} to target_files")

# Move one file
shutil.move(str(file2), str(target_dir / file2.name))
print(f"Moved {file2.name} to target_files")