from pathlib import Path

file_path = Path(__file__).parent / "demofile.txt"

with open(file_path, "r", encoding="utf-8") as f:
    print(f.read())
    print(f.read(5))
    print(f.readline())
    print(f.readline())

