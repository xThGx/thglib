import json
import os

DATA_FILE = "pflegeheime_daten.json"
BETTEN_KATEGORIEN = ["klein", "mittel", "gross"]

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def print_header(title):
    print("\n" + "=" * 50)
    print(f" {title.upper()}")
    print("=" * 50)

def heim_hinzufuegen(data):
    print_header("Neues Pflegeheim anlegen")
    name = input("Name des Pflegeheims: ").strip()
    if not name:
        print("[-] Name darf nicht leer sein.")
        return

    if name in data:
        print("[-] Ein Pflegeheim mit diesem Namen existiert bereits.")
        return

    data[name] = {kat: {} for kat in BETTEN_KATEGORIEN}
    save_data(data)
    print(f"[+] Pflegeheim '{name}' erfolgreich angelegt.")

def heime_auflisten(data):
    print_header("Übersicht aller Pflegeheime")
    if not data:
        print("Keine Pflegeheime erfasst.")
        return

    for name, kat_data in data.items():
        print(f"\n🏠 Pflegeheim: {name}")
        for kat in BETTEN_KATEGORIEN:
            ausgaben = kat_data.get(kat, {})
            gesamtsumme = sum(ausgaben.values())
            print(f"  └ Bettengröße [{kat.upper()}]: {gesamtsumme:.2f} € Gesamt ({len(ausgaben)} Positionen)")

def heim_bearbeiten(data):
    print_header("Pflegeheim bearbeiten")
    if not data:
        print("Keine Pflegeheime vorhanden.")
        return

    heime = list(data.keys())
    for idx, name in enumerate(heime, 1):
        print(f"{idx}. {name}")

    try:
        wahl = int(input("\nWähle ein Pflegeheim (Nummer): ")) - 1
        if wahl < 0 or wahl >= len(heime):
            print("[-] Ungültige Auswahl.")
            return
    except ValueError:
        print("[-] Bitte eine Zahl eingeben.")
        return

    heim_name = heime[wahl]

    while True:
        print(f"\n--- Bearbeite: {heim_name} ---")
        print("1. Ausgaben für Bettengröße verwalten")
        print("2. Heim umbenennen")
        print("3. Heim löschen")
        print("4. Zurück zum Hauptmenü")

        sub_wahl = input("Auswahl: ").strip()

        if sub_wahl == "1":
            ausgaben_verwalten(data, heim_name)
        elif sub_wahl == "2":
            neuer_name = input("Neuer Name: ").strip()
            if neuer_name and neuer_name not in data:
                data[neuer_name] = data.pop(heim_name)
                save_data(data)
                heim_name = neuer_name
                print("[+] Name geändert.")
            else:
                print("[-] Name ungültig oder bereits vergeben.")
        elif sub_wahl == "3":
            bestaetigung = input(f"Sicher, dass '{heim_name}' gelöscht werden soll? (j/n): ")
            if bestaetigung.lower() == 'j':
                del data[heim_name]
                save_data(data)
                print("[+] Pflegeheim gelöscht.")
                break
        elif sub_wahl == "4":
            break

def ausgaben_verwalten(data, heim_name):
    print(f"\nBettengröße wählen für '{heim_name}':")
    for idx, kat in enumerate(BETTEN_KATEGORIEN, 1):
        print(f"{idx}. {kat.capitalize()}")

    try:
        k_wahl = int(input("Auswahl: ")) - 1
        if k_wahl < 0 or k_wahl >= len(BETTEN_KATEGORIEN):
            print("[-] Ungültige Kategorie.")
            return
    except ValueError:
        print("[-] Bitte eine Zahl eingeben.")
        return

    kategorie = BETTEN_KATEGORIEN[k_wahl]
    ausgaben = data[heim_name][kategorie]

    while True:
        print(f"\n--- Ausgaben [{kategorie.upper()}] für '{heim_name}' ---")
        if not ausgaben:
            print("Keine Ausgaben erfasst.")
        else:
            for pos, betrag in ausgaben.items():
                print(f"  • {pos}: {betrag:.2f} €")
            print(f"  Gesamtsumme: {sum(ausgaben.values()):.2f} €")

        print("\nOptionen:")
        print("1. Ausgabenposition hinzufügen / ändern")
        print("2. Ausgabenposition löschen")
        print("3. Zurück")

        opt = input("Auswahl: ").strip()

        if opt == "1":
            pos_name = input("Bezeichnung der Ausgabe (z.B. Personal, Verpflegung, Strom): ").strip()
            if not pos_name:
                continue
            try:
                betrag = float(input(f"Betrag (€) für '{pos_name}': "))
                ausgaben[pos_name] = betrag
                save_data(data)
                print("[+] Ausgabe gespeichert.")
            except ValueError:
                print("[-] Ungültiger Betrag.")
        elif opt == "2":
            pos_name = input("Welche Position löschen?: ").strip()
            if pos_name in ausgaben:
                del ausgaben[pos_name]
                save_data(data)
                print("[+] Position entfernt.")
            else:
                print("[-] Position nicht gefunden.")
        elif opt == "3":
            break

def main():
    data = load_data()

    while True:
        print_header("Pflegeheim Ausgaben-Manager")
        print("1. Pflegeheime & Ausgaben auflisten")
        print("2. Neues Pflegeheim anlegen")
        print("3. Pflegeheim / Ausgaben bearbeiten")
        print("4. Beenden")

        choice = input("\nWähle eine Option (1-4): ").strip()

        if choice == "1":
            heime_auflisten(data)
        elif choice == "2":
            heim_hinzufuegen(data)
        elif choice == "3":
            heim_bearbeiten(data)
        elif choice == "4":
            print("\nProgramm beendet. Auf Wiedersehen!")
            break
        else:
            print("[-] Ungültige Eingabe.")

if __name__ == "__main__":
    main()