from pathlib import Path

# Specify the directory path
directory = Path(__file__).resolve().parent  # Use the current file's directory

# List only files in the top-level directory
#files = [item for item in directory.iterdir() if item.is_file()]

# List all files recursively in the directory and its subdirectories
recursive_files = [item for item in directory.rglob("*") if item.is_file()]

item_count: int = len(recursive_files) 

print(F"{recursive_files}\n")
print(f"Total number of files found: {item_count}")
input("Press Enter to exit...") 