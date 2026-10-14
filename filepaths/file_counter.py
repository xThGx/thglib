from pathlib import Path

def count_files(destination_folder: str | Path = ".") -> int:
    """Zählt alle Dateien in einem Ordner und dessen Unterordnern."""
    directory = Path(destination_folder).resolve()
    
    # Nutzt direkt len(), das spart die for-Schleife
    recursive_files = [item for item in directory.rglob("*") if item.is_file()]
    
    return len(recursive_files)

if __name__ == "__main__":
    folder_path = input("Geben Sie den Pfad zum Ordner ein (oder drücken Sie Enter für das aktuelle Verzeichnis): ")
    if not folder_path:
        folder_path = "."
    
    file_count = count_files(folder_path)
    print()
    print(f"Dateien im Ordner: {file_count}")
    print()
    input("Drücken Sie Enter, um das Programm zu beenden...")