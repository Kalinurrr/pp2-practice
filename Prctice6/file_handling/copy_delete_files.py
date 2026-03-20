from pathlib import Path
import os

file_path = Path(__file__).parent / "demofile.txt"

if os.path.exists(file_path):
    os.remove(file_path)
    print("File deleted successfully.")
else:
    print("The file does not exist.")


"""In Python, we use os.remove() to delete a file.
Before deleting, it is better to check with os.path.exists() so that the program does not crash.
To delete a folder, we use os.rmdir(), but it only works for empty folders."""