import json
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


def item_count(file_paths) -> str:
    i = len(file_paths)
    return f"\n {i} Files found \n"


def search_for(search_term: str, path_list: list[str]) -> list[str]:
    fending = []
    for path in path_list:
        if search_term in path:
            fending.append(path)
    return fending


if __name__ == "__main__":
    # Example usage
    input_path = input("Geben Sie den Pfad zum Ordner ein: ")
    items = []
    path_list = list_files_from_path(input_path)
    i = len(path_list)
    print()
    print(f"{i} Files found.")
    print()
    while True:
        print("=" * 25)
        print("1. Choose new folder")
        print("2. Sort for file ending?")
        print("3. Print Paths in CLI")
        print("4. Create and save JSON file")
        print("5. Clear searchterm")
        print("Enter 'c, e, x, exit, end, close' to exit the script")
        print("-" * 25)
        print()
        desicion = input("Choose what to do: ").lower().strip()
        print()

        match desicion:
            case "1":
                input_path = input("Geben Sie den Pfad zum Ordner ein: ")
                path_list = list_files_from_path(input_path)
                print(item_count(path_list))
            case "2":
                search_term = input("What are you searching for? ")
                items = search_for(search_term, path_list)
                print(item_count(items))
            case "3":
                if items == []:
                    for path in path_list:
                        print(path)
                    print(item_count(path_list))
                else:
                    for item in items:
                        print(item)
                    print(item_count(items))

            case "4":
                if items == []:
                    # JSON-Datei im Schreibmodus ('w') öffnen und speichern
                    with open("filePaths.json", "w", encoding="utf-8") as f:
                        json.dump(path_list, f, ensure_ascii=False, indent=4)
                else:
                    # JSON-Datei im Schreibmodus ('w') öffnen und speichern
                    with open("filePaths.json", "w", encoding="utf-8") as f:
                        json.dump(items, f, ensure_ascii=False, indent=4)

                print("file safed successfully")
            case "5":
                items = []
            case "exit" | "e" | "end" | "close" | "c" | "x":
                break
            case _:
                print("Enter a valid parameter from the list")
