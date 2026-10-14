import sqlite3
from datetime import datetime
import pwinput
import getpass
import bcrypt
from contextlib import closing, contextmanager

DB_NAME = "users.db"

'''
def get_connection():
    """Hilfsfunktion für die Datenbankverbindung."""
    return sqlite3.connect(DB_NAME)
'''
@contextmanager
def get_db():
    """Öffnet die Verbindung, führt ein Commit/Rollback aus und schließt sie garantiert."""
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
        conn.commit()  # Automatisches Commit bei Erfolg
    except Exception:
        conn.rollback()  # Automatischer Rollback bei Fehler
        raise
    finally:
        conn.close()  # Garantiertes Schließen am Ende

def db_init():
    """Erstellt die Datenbank und die Tabelle, falls sie noch nicht existieren."""
    with get_db() as verbindung:
        with verbindung:
            zeiger = verbindung.cursor()
            zeiger.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    key INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE CHECK(email LIKE '%@%.%'),
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                last_login TEXT,
                is_admin BOOLEAN NOT NULL DEFAULT 0,
                is_active BOOLEAN NOT NULL DEFAULT 1
            )
            """
        )
        '''
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
    
        #verbindung.commit()
        #verbindung.close()
        '''

def user_create(firstname: str, lastname: str, email: str, password_cleartext: str):
    """Erstellt einen neuen User in der Datenbank."""
    if not firstname or not lastname or not email or not password_cleartext:
        return False, "Bitte alle Felder ausfüllen."

    # Passwort sicher hashen
    bytes_passwort = password_cleartext.encode("utf-8")
    hash_wert = bcrypt.hashpw(bytes_passwort, bcrypt.gensalt())
    hash_text = hash_wert.decode("utf-8")

    try:
        with get_db() as verbindung:
            with verbindung:  # Führt automatisch COMMIT oder ROLLBACK aus
                zeiger = verbindung.cursor()
                zeiger.execute(
                """
                INSERT INTO users (firstname, lastname, email, password_hash)
                VALUES (?, ?, ?, ?)
                """,
                (firstname.strip(), lastname.strip(), email.strip().lower(), hash_text)
            )
            return True, f"User '{firstname} {lastname}' erfolgreich angelegt!"
    except sqlite3.IntegrityError:
        return False, f"E-Mail '{email}' existiert bereits oder ist ungültig."
    except Exception as e:
        return False, f"Fehler beim Anlegen des Users: {str(e)}"

def user_password_check(email: str, password_cleartext: str) -> tuple[bool, str, dict | None]:
    """
    Prüft E-Mail, Passwort und Aktivitätsstatus.
    Rückgabe: (Erfolg, Nachricht, User-Daten als Dict oder None)
    """
    try:
        with get_db() as verbindung:
            with verbindung:
                zeiger = verbindung.cursor()
                zeiger.execute(
                    '''
                    SELECT password_hash, is_active, firstname, lastname, is_admin 
                    FROM users WHERE email = ?
                    ''',
                    (email.strip().lower(),)
                )
                ergebnis = zeiger.fetchone()

            if not ergebnis:
                return False, "E-Mail oder Passwort falsch.", None
        
            gespeicherter_hash, is_active, firstname, lastname, is_admin = ergebnis

            if not is_active:
                return False, "User ist deaktiviert.", None
        
            bytes_password = password_cleartext.encode("utf-8")
            if bcrypt.checkpw(bytes_password, gespeicherter_hash.encode("utf-8")):
                # Last Login Aktualisieren
                last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                zeiger.execute(
                    "UPDATE users SET last_login = ? WHERE email = ?",
                    (last_login, email.strip().lower())
                )
                user_info = {
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email,
                    "is_admin": bool(is_admin)
                }
                return True, "Login erfolgreich!", user_info
            else:
                return False, "E-Mail oder Passwort falsch.", None
    except Exception as e:
        return False, f"Fehler bei der Anmeldung: {str(e)}", None

def user_get_all(active_only: bool = False) -> list[dict]:
    """Holt alle User als Liste von Dictionaries für Tabellenansichten in der GUI."""
    query = """
        SELECT key, firstname, lastname, email, created_at, last_login, is_admin, is_active 
        FROM users
    """
    if active_only:
        query += " WHERE is_active = 1"
    query += " ORDER BY lastname, firstname"

    with get_db() as verbindung:
        with verbindung:
            zeiger = verbindung.cursor()
            zeiger.execute(query)
            rows = zeiger.fetchall()

    users = []

    for row in rows:
        users.append({
            "id": row[0],
            "firstname": row[1],
            "lastname": row[2],
            "email": row[3],
            "created_at": row[4],
            "last_login": row[5] or "Noch nie",
            "is_admin": bool(row[6]),
            "is_active": bool(row[7])
        })
    return users

'''
def user_show_active():
    """Zeigt alle aktiven User an."""
    with get_db() as verbindung:
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
'''
    
def user_password_change(email, altes_passwort_cleartext, neues_passwort_cleartext):
    """Ändert das Passwort eines Users nach Validierung des alten Passworts."""
    success, msg, _ = user_password_check(email, altes_passwort_cleartext)
    if not success:
        return False, f"Passwortänderung fehlgeschlagen: {msg}"
    
    neuer_hash = bcrypt.hashpw(neues_passwort_cleartext.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    with get_db() as verbindung:
        with verbindung:
            zeiger = verbindung.cursor()
            zeiger.execute(
                "UPDATE users SET password_hash = ? WHERE email = ?",
                (neuer_hash, email.strip().lower())
            )
    return True, "Passwort erfolgreich geändert!"

def user_set_active_status(email: str, is_active: bool) -> tuple[bool, str]:
    """Aktiviert oder deaktiviert einen User."""
    status_int = 1 if is_active else 0
    status_text = "aktiviert" if is_active else "deaktiviert"

    with get_db() as verbindung:
        with verbindung:
            zeiger = verbindung.cursor()
            zeiger.execute(
                "UPDATE users SET is_active = ? WHERE email = ?",
                (status_int, email.strip().lower())
            )
        if zeiger.rowcount > 0:
            return True, f"User '{email}' wurde {status_text}."
        return False, f"Kein User mit E-Mail '{email}' gefunden."

# --- Hauptprogramm (Konsolen-Benutzeroberfläche) ---
if __name__ == "__main__":
    db_init()

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
            users = user_get_all()
            for user in users:
                print(f"ID: {user['id']}, Name: {user['firstname']} {user['lastname']}, E-Mail: {user['email']}")
        elif choice == "3":
            email = input("E-Mail: ")
            password = pwinput.pwinput("Passwort: ", mask='*')
            user_password_check(email, password)
        elif choice == "4":
            email = input("E-Mail: ")
            altes_passwort = pwinput.pwinput("Aktuelles Passwort: ", mask='*')
            neues_passwort = pwinput.pwinput("Neues Passwort: ", mask='*')
            user_password_change(email, altes_passwort, neues_passwort)
        elif choice == "5":
            email = input("E-Mail des zu löschenden Users: ")
            user_set_active_status(email, False)
        elif choice == "6":
            print("Tschüss! Bis morgen.")
            break
        else:
            print("Ungültige Auswahl. Bitte gib 1, 2, 3, 4, 5 oder 6 ein.")
