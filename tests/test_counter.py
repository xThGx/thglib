from ..filepaths.file_counter import count_files

def test_file_count_leerer_ordner(tmp_path):
    # Test 1: Ein komplett leerer Ordner sollte 0 zurückgeben
    anzahl = count_files(tmp_path)
    assert anzahl == 0

def test_file_count_mit_dateien(tmp_path):
    # Test 2: Wir erstellen 3 Testdateien (auch im Unterordner)
    (tmp_path / "datei1.txt").write_text("Inhalt")
    (tmp_path / "datei2.log").write_text("Inhalt")
    
    unterordner = tmp_path / "ordner"
    unterordner.mkdir()
    (unterordner / "datei3.pdf").write_text("Inhalt")
    
    # Jetzt rufen wir deine Funktion auf
    anzahl = count_files(tmp_path)
    
    # assert prüft, ob das Ergebnis stimmt (3 Dateien)
    assert anzahl == 3
