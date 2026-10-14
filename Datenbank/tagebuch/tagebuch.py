import sqlite3
from datetime import datetime


def datenbank_initialisieren():
    """Erstellt die Datenbank und die Tabelle, falls sie noch nicht existieren."""
    verbindung = sqlite3.connect("tagebuch.db")
    zeiger = verbindung.cursor()

    # Tabelle für die Einträge erstellen
    # Das DATUM (YYYY-MM-DD) nutzen wir als PRIMARY KEY (eindeutiger Schlüssel)
    zeiger.execute(
        """
        CREATE TABLE IF NOT EXISTS eintraege (
            datum TEXT PRIMARY KEY,
            inhalt TEXT NOT NULL
        )
    """
    )

    verbindung.commit()
    verbindung.close()


def eintrag_speichern(text):
    """Speichert den Text für das aktuelle Datum.

    Existiert schon ein Eintrag, wird der neue Text angehängt.
    """
    # Aktuelles Datum im Format JAHR-MONAT-TAG holen
    heute = datetime.now().strftime("%Y-%m-%d")

    verbindung = sqlite3.connect("tagebuch.db")
    zeiger = verbindung.cursor()

    # Nachsehen, ob heute schon etwas geschrieben wurde
    zeiger.execute("SELECT inhalt FROM eintraege WHERE datum = ?", (heute,))
    ergebnis = zeiger.fetchone()

    if ergebnis:
        # Wenn schon ein Eintrag existiert, neuen Text mit Zeilenumbruch anhängen
        neuer_inhalt = ergebnis[0] + "\n" + text
        zeiger.execute(
            "UPDATE eintraege SET inhalt = ? WHERE datum = ?",
            (neuer_inhalt, heute),
        )
        print(f"\n[Info] Eintrag zum heutigen Datum ({heute}) hinzugefügt!")
    else:
        # Wenn es der erste Eintrag heute ist, neu anlegen
        zeiger.execute(
            "INSERT INTO eintraege (datum, inhalt) VALUES (?, ?)",
            (heute, text),
        )
        print(f"\n[Info] Neuer Eintrag für heute ({heute}) erstellt!")

    verbindung.commit()
    verbindung.close()


def eintraege_anzeigen():
    """Zeigt alle bisherigen Tagebucheinträge an."""
    verbindung = sqlite3.connect("tagebuch.db")
    zeiger = verbindung.cursor()

    zeiger.execute("SELECT datum, inhalt FROM eintraege ORDER BY datum DESC")
    alle_eintraege = zeiger.fetchall()

    print("\n--- DEINE BISHERIGEN EINTRÄGE ---")
    if not alle_eintraege:
        print("Noch keine Einträge vorhanden.")
    for datum, inhalt in alle_eintraege:
        print(f"\nDatum: {datum}")
        print(f"Aktivitäten:\n{inhalt}")
        print("-" * 30)

    verbindung.close()


# --- Hauptprogramm (Konsolen-Benutzeroberfläche) ---
if __name__ == "__main__":
    datenbank_initialisieren()

    while True:
        print("\nTagebuch-App")
        print("1: Neuer Eintrag")
        print("2: Bisherige Einträge anzeigen")
        print("3: Beenden")

        auswahl = input("Wähle eine Option (1-3): ").strip()

        if auswahl == "1":
            was_getan = input("\nWas hast du heute gemacht? ")
            if was_getan:
                eintrag_speichern(was_getan)
        elif auswahl == "2":
            eintraege_anzeigen()
        elif auswahl == "3":
            print("Tschüss! Bis morgen.")
            break
        else:
            print("Ungültige Auswahl. Bitte gib 1, 2 oder 3 ein.")
