from pathlib import Path

file_path = Path(__file__).parent / "demofile.txt"
with open(file_path, "a", encoding="utf-8") as f:
    f.write("\nNow the file has more content!")
    f.write("\nI added this text")
with open(file_path, "r", encoding="utf-8") as f:
    print(f.read())

#write "w"
from pathlib import Path
file_path = Path(__file__).parent / "demofile.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write("Woops! I have deleted the content!")
with open(file_path, "r", encoding="utf-8") as f:
    print(f.read())



from pathlib import Path

file_path = Path(__file__).parent / "myfile.txt"
with open(file_path, "x", encoding="utf-8") as f:
    f.write("This is a new file.")
print("New file created successfully.")