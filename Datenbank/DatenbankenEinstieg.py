from dbm import sqlite3
from datetime import datetime

def datenbank_initialisieren():
    """Erstellt die Datenbank und die Tabelle, falls sie noch nicht existieren."""
    verbindung = sqlite3.connect("user.db")
    zeiger = verbindung.cursor()

    # Tabelle für die Benutzer erstellen
    # Das DATUM (YYYY-MM-DD) nutzen wir als PRIMARY KEY (eindeutiger Schlüssel)
    zeiger.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            key INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """
    )

    verbindung.commit()
    verbindung.close()