import sqlite3
from datetime import datetime
import pwinput
import getpass
import bcrypt


def datenbank_initialisieren():
    """Erstellt die Datenbank und die Tabelle, falls sie noch nicht existieren."""
    verbindung = sqlite3.connect("users_hashPW.db")
    zeiger = verbindung.cursor()

    # Tabelle für die Einträge erstellen
    # Das DATUM (YYYY-MM-DD) nutzen wir als PRIMARY KEY (eindeutiger Schlüssel)
    zeiger.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            key INTEGER PRIMARY KEY,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE check(email LIKE '%@%.%'),
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            last_login TEXT,
            is_admin BOOLEAN NOT NULL DEFAULT 0,
            is_active BOOLEAN NOT NULL DEFAULT 1
        )
    """
    )

    # 2. Bestehende Spalten auslesen
    zeiger.execute("PRAGMA table_info(users)")
    existing_columns = {row[1] for row in zeiger.fetchall()}


    # 3. Soll-Spalten definieren, die im Laufe der Zeit dazukommen könnten
    #if add columns is empty the foor loop will be skipped
    add_columns = {
        #"last_login": "TEXT",
        #"is_admin": "BOOLEAN",
        #"is_active": "BOOLEAN",
        #"phone_number": "TEXT",
        #"profile_picture": "BLOB",
    }

    # 4. Fehlende Spalten hinzufügen
    if add_columns:
        for column_name, column_type in add_columns.items():
            if column_name not in existing_columns:
                zeiger.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
    
    verbindung.commit()
    verbindung.close()


def user_create(firstname, lastname, email, password_cleartext):
    """Erstellt einen neuen User in der Datenbank."""
    verbindung = sqlite3.connect("users_hashPW.db")
    zeiger = verbindung.cursor()
    
    # 1. Passwort sicher mit bcrypt hashen
    bytes_passwort = password_cleartext.encode("utf-8")
    hash_wert = bcrypt.hashpw(bytes_passwort, bcrypt.gensalt())

    # 2. Den Byte-Hash in Text umwandeln für SQLite
    hash_text = hash_wert.decode("utf-8")

    last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        zeiger.execute(
            "INSERT INTO users (firstname, lastname, email, password_hash, last_login) VALUES (?, ?, ?, ?, ?)",
            (firstname, lastname, email, hash_text, last_login)
        )
        verbindung.commit()
        print(f"\n[Info] User '{firstname} {lastname}' erfolgreich angelegt!")
    except sqlite3.IntegrityError:
        print(f"\n[Error] E-Mail '{email}' existiert bereits oder ist ungültig.")
    finally:
        verbindung.close()

def user_show_all():
    """Zeigt alle bisherigen User an."""
    verbindung = sqlite3.connect("users_hashPW.db")
    zeiger = verbindung.cursor()

    zeiger.execute("SELECT firstname, lastname, email, last_login FROM users ORDER BY lastname, firstname")
    alle_eintraege = zeiger.fetchall()

    print("\n--- DEINE BISHERIGEN USER ---")
    if not alle_eintraege:
        print("Noch keine User vorhanden.")
    for firstname, lastname, email, last_login in alle_eintraege:
        print(f"\nName: {firstname} {lastname}")
        print(f"E-Mail: {email}")
        print(f"Letzter Login: {last_login}")
        print("-" * 30)

    verbindung.close()

def user_show_active():
    """Zeigt alle aktiven User an."""
    verbindung = sqlite3.connect("users_hashPW.db")
    zeiger = verbindung.cursor()

    zeiger.execute("SELECT firstname, lastname, email, last_login FROM users WHERE is_active = 1 ORDER BY lastname, firstname")
    aktive_eintraege = zeiger.fetchall()

    print("\n--- AKTIVE USER ---")
    if not aktive_eintraege:
        print("Noch keine User vorhanden.")
    for firstname, lastname, email, last_login in aktive_eintraege:
        print(f"\nName: {firstname} {lastname}")
        print(f"E-Mail: {email}")
        print(f"Letzter Login: {last_login}")
        print("-" * 30)

    verbindung.close()

def user_passwort_check(email, password_cleartext)-> bool:
    """Prüft, ob das eingegebene Passwort mit dem gespeicherten Hash übereinstimmt."""
    verbindung = sqlite3.connect("users_hashPW.db")
    zeiger = verbindung.cursor()

    zeiger.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
    ergebnis = zeiger.fetchone()

    if ergebnis:
        gespeicherter_hash = ergebnis[0].encode("utf-8")
        bytes_passwort = password_cleartext.encode("utf-8")
        if bcrypt.checkpw(bytes_passwort, gespeicherter_hash):
            last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            zeiger.execute(
                "UPDATE users SET last_login = ? WHERE email = ?",
                (last_login, email)
            )
            print("\n[Info] Passwort korrekt!")
            verbindung.close()
            return True
        else:
            print("\n[Error] Falsches Passwort.")
            verbindung.close()
            return False
    else:
        print("\n[Error] E-Mail nicht gefunden.")
        verbindung.close()
        return False

def user_password_change(email, altes_passwort_cleartext, neues_passwort_cleartext):
    """Ändert das Passwort eines Users, wenn das alte Passwort korrekt ist."""
    if user_passwort_check(email, altes_passwort_cleartext):
        verbindung = sqlite3.connect("users_hashPW.db")
        zeiger = verbindung.cursor()

        # Neues Passwort hashen
        bytes_neues_passwort = neues_passwort_cleartext.encode("utf-8")
        neuer_hash_wert = bcrypt.hashpw(bytes_neues_passwort, bcrypt.gensalt())
        neuer_hash_text = neuer_hash_wert.decode("utf-8")

        zeiger.execute(
            "UPDATE users SET password_hash = ? WHERE email = ?",
            (neuer_hash_text, email)
        )
        verbindung.commit()
        verbindung.close()
        print("\n[Info] Passwort erfolgreich geändert!")

def user_deaktivate(email):
    """Deaktiviert einen User in der Datenbank."""
    verbindung = sqlite3.connect("users_hashPW.db")
    zeiger = verbindung.cursor()

    zeiger.execute("UPDATE users SET is_active = 0 WHERE email = ?", (email,))
    if zeiger.rowcount > 0:
        print(f"\n[Info] User mit E-Mail '{email}' wurde gelöscht.")
    else:
        print(f"\n[Error] Kein User mit E-Mail '{email}' gefunden.")

    verbindung.commit()
    verbindung.close()

def user_reactivate(email):
    """Aktiviert einen User in der Datenbank."""
    verbindung = sqlite3.connect("users_hashPW.db")
    zeiger = verbindung.cursor()

    zeiger.execute("UPDATE users SET is_active = 1 WHERE email = ?", (email,))
    if zeiger.rowcount > 0:
        print(f"\n[Info] User mit E-Mail '{email}' wurde aktiviert.")
    else:
        print(f"\n[Error] Kein User mit E-Mail '{email}' gefunden.")

    verbindung.commit()
    verbindung.close()

# --- Hauptprogramm (Konsolen-Benutzeroberfläche) ---
if __name__ == "__main__":
    datenbank_initialisieren()

    while True:
        print("\n------ USER VERWALTUNG ------")
        print("1: Neuen User anlegen")
        print("2: Angelegte User anzeigen")
        print("3: Passwort prüfen")
        print("4: Passwort ändern")
        print("5: User deaktivieren")
        print("6: Beenden")
        print("-" * 29)

        choice = input("Wähle eine Option (1-6): ").strip()

        if choice == "1":
            firstname = input("Vorname: ")
            lastname = input("Nachname: ")
            email = input("E-Mail: ")
            password = pwinput.pwinput("Passwort: ", mask='*')
            user_create(firstname, lastname, email, password)
        elif choice == "2":
            user_show_active()
        elif choice == "3":
            email = input("E-Mail: ")
            password = pwinput.pwinput("Passwort: ", mask='*')
            user_passwort_check(email, password)
        elif choice == "4":
            email = input("E-Mail: ")
            altes_passwort = pwinput.pwinput("Aktuelles Passwort: ", mask='*')
            neues_passwort = pwinput.pwinput("Neues Passwort: ", mask='*')
            user_password_change(email, altes_passwort, neues_passwort)
        elif choice == "5":
            email = input("E-Mail des zu löschenden Users: ")
            user_deaktivate(email)
        elif choice == "6":
            print("Tschüss! Bis morgen.")
            break
        else:
            print("Ungültige Auswahl. Bitte gib 1, 2, 3, 4, 5 oder 6 ein.")
