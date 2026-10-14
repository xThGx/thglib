import os
from pathlib import Path


def list_files(
    parent_directory: dict[str, dict | None], current_filepath: str = ""
) -> list[str]:

    file_paths = []

    for file_name, dir in parent_directory.items():
        new_filepath: str = f"{current_filepath + os.sep}{file_name}" if current_filepath else f"{os.sep}{file_name}"

        if dir is None:
            file_paths.append(new_filepath)
        else:
            file_paths.extend(list_files(dir, new_filepath))
            
    return file_paths




if __name__ == "__main__":
    # Example usage
    directory_structure = {
        "folder1": {
            "file1.txt": None,
            "file2.txt": None,
            "subfolder1": {
                "file3.txt": None
            }
        },
        "folder2": {
            "file4.txt": None
        },
        "file5.txt": None
    }
    path: str = str(Path(__file__).resolve().parent)
    all_file_paths = list_files(directory_structure, path)        
    for pat in all_file_paths:
        print(pat)
    
    input("Press Enter to exit...")