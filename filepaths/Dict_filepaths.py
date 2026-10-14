import os
from pathlib import Path


def list_files_from_path(target_path: str) -> list[str]:
    file_paths = []
    if not Path(target_path).exists():
        return []
    # os.walk durchsucht den Pfad und alle Unterordner rekursiv
    for root, dirs, files in os.walk(target_path):
        for file in files:
            # Vollständigen Pfad zur Liste hinzufügen
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
            
    return file_paths


if __name__ == "__main__":
    # Example usage
    input_path = input("Geben Sie den Pfad zum Ordner ein: ")
    
    path_list = list_files_from_path(input_path)
    
    print()

    for path in path_list:
        print(path)
    #print(list_files_from_path(input_path))
    print()
    print(f"{len(path_list)} Files found.")
    print()
    input("Press Enter to exit...")