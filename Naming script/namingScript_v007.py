import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

def dateien_umbenennen():
    """Dieses Skript ändert den Dateinamen  """
    # RIGOROSE PFADERMITTLUNG FÜR PYINSTALLER (.exe):
    if getattr(sys, 'frozen', False):
        # Läuft als kompilierte .exe -> Ordner nehmen, in dem die .exe liegt
        ordner = Path(sys.executable).resolve().parent
    else:
        # Läuft als normales .py Skript -> Ordner nehmen, in dem die .py Datei liegt
        ordner = Path(__file__).resolve().parent
        
    
    print(f"=== Dateiumbenennung mit dynamischem Index in: {ordner} ===\n")
    
    # Benutzereingaben
    endung = input("Welche Dateiendung soll verarbeitet werden? (z.B. txt, jpg): ").strip().lstrip('.') #input() gibt consolen eingaben weiter & strip() löscht alle Leerzeichen & lstrip('.') löscht alle '.'  
    eingabe = input("Soll ein Datumspräfix verwendet werden?: ").strip().lower()
    dateUse = eingabe in ["j", "ja", "y", "yes"]
    if dateUse:
        pattern = input("Wie soll die Datei nach dem Datumspräfix heißen? (z.B. 2026-09-25_'Projektnummer'): ").strip()
    else:
        pattern = input("Wie soll die Datei heißen? (z.B. 'Projektnummer'): ").strip()
    
    # Abbruch bei keiner Eingabe
    if not endung or not pattern:
        print("Ungültige Eingabe! Abbruch.")
        return

    # Passende Dateien suchen und sortieren
    dateien = sorted(list(ordner.glob(f"*.{endung}"))) # Erstellt eine sortierte Liste aus ."EingegebeneDateiendung" das * bezieht sich darauf das der Name vor der Dateiendung egal ist
    #print(dateien)
    
    # Skript-Datei selbst ausfiltern
    skript_datei = Path(__file__).resolve() # Erzeugen des relativen Dateipfades wo das Skript liegt (Bsp. hier wird 'C:\Users\Administrator\Desktop\Test\*DATEINAME*.endung' erzeugt wenn das Skript im Desktop Ordner Test liegt)
    dateien = [d for d in dateien if d != skript_datei] # Erstelle neue Liste, d Representiert den 'Dateipfad' mit dateinamen und wird nur in die neue Liste aufgenommen wenn er nicht gleich dem Skriptpfad ist (also nicht das Skript selbst ist)
    #print(dateien)

    # Abbruch wenn die Liste leer ist
    if not dateien:
        print(f"Keine .{endung}-Dateien im Ordner gefunden.")
        return

    # SCHRITT 1.: Basis-Namen generieren und Duplikate zählen
    basis_namen = []
    for datei in dateien: 
        aenderungs_timestamp = datei.stat().st_mtime # .stat() holt spezifische Metadaten von der Datei selbst (Hier hole ich st_mtime -> Modification time) es gibt noch size, atime(acces time) und ctime(creation time) 
        if dateUse:
            aenderungs_datum = datetime.fromtimestamp(aenderungs_timestamp).strftime('%Y-%m-%d_%H%M') # Datetime formatieren wie es gebraucht wird 'YYYY-MM-DD_HHMM'
        
            # Der reine Name ohne Index (z.B. "2026-09-25_1806_Projektnummer")
            basis_name = f"{aenderungs_datum}_{pattern}"
        else:
            basis_name = f"{pattern}"

        basis_namen.append((datei, basis_name)) # Liste komplett zusammen bauen > Dateipfad und namen zusammenfügen
        #print(basis_namen)

    # Zählen, wie oft welcher Basis-Name vorkommt
    namens_zähler = Counter(b_name for _, b_name in basis_namen) # Erstellt eine Liste [dateiname: anzahl vorkommen, ..., n]
    
    # Laufende Nummer für Namen mit Mehrfachvorkommen speichern
    aktueller_index = {}

    # SCHRITT 2.: Finale Dateinamen zusammenbauen
    umbenennungen = []
    for datei, basis_name in basis_namen:
        # Kommt der gleiche Name öfter als 1-mal vor wird ein index dazu gebaut -> _idx_02d (zweistellige dezimal zahl wenn idx == 1 wird daraus 01)
        if namens_zähler[basis_name] > 1:
            # Index hochzählen (startet bei 1)
            aktueller_index[basis_name] = aktueller_index.get(basis_name, 0) + 1
            idx = aktueller_index[basis_name]
            neuer_name = f"{basis_name}_{idx:02d}.{endung}"
        else:
            # Eindeutiger Name -> KEIN Index
            neuer_name = f"{basis_name}.{endung}"

        neuer_pfad = ordner / neuer_name
        umbenennungen.append((datei, neuer_pfad, neuer_name))
        #print(umbenennungen)

    # --- VORSCHAU (DRY-RUN) ---
    print(f"\nVORSCHAU: Folgende {len(umbenennungen)} Datei(en) werden umbenannt:\n")
    print("-" * 120)
    for alter_pfad, _, neuer_name in umbenennungen:
        print(f"  {alter_pfad.name:<25}     ➔   {neuer_name}")
    print("-" * 120)

    # Bestätigung abfragen
    bestaetigung = input("\nSollen diese Änderungen durchgeführt werden? (j/n oder y/n): ").strip().lower()
    
    if bestaetigung not in ['j', 'ja', 'y', 'yes']:
        print("Vorgang abgebrochen. Es wurden keine Dateien verändert.")
        return

    # --- UMBENENNUNG DURCHFÜHREN ---
    print("\nUmbenennung läuft...")
    erfolgreich = 0
    
    for alter_pfad, neuer_pfad, neuer_name in umbenennungen:
        # Prüfen, ob Zieldatei bereits existiert
        if neuer_pfad.exists() and neuer_pfad != alter_pfad:
            print(f"Übersprungen (Datei existiert bereits): {neuer_name}")
            continue
            
        alter_pfad.rename(neuer_pfad)
        erfolgreich += 1

    print(f"\nFertig! {erfolgreich} von {len(umbenennungen)} Datei(en) wurden umbenannt.")

if __name__ == "__main__":
    dateien_umbenennen()
    closeTimer = 2.0
    print("\n")
    print("-" * 120)
    print(f"\nSkript schließt sich in {closeTimer} Sekunden.")
    time.sleep(closeTimer)