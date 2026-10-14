'''
This is a simple Python program to manage care homes and their bed counts. It allows users to create care homes, view information about them, and edit the occupancy status of beds.
'''
__version__ = "1.0.0"
##################################################################################################################################################
# Namespace: main.py
care_homes = {}  # Dictionary to store care home names and their bed counts


##################################################################################################################################################

def current_version():
    return __version__

def info():
    if not care_homes:
        print("Es sind keine Pflegeheime angelegt.")
        return
    print("Angelegte Pflegeheime:")
    for name, details in care_homes.items():
        beds = details["Betten"]
        print(f"- {name}: {beds} Betten")
        show_beds = input(f"Möchten Sie die Bettenliste anzeigen? (ja/nein): ").lower()
        if show_beds in ["j", "y", "ja", "yes"]:
            print(f"Betten Status für '{name}':")
            for bed_number, occupant in details["Bettliste"].items():
                status = "Belegt" if occupant else "Frei"
                print(f"  - Bett {bed_number}: {status}")
    return

def edit_care_home():
    if not care_homes:
        print("Es sind keine Pflegeheime angelegt.")
        return
    care_home_name = input("Bitte geben Sie den Namen des Pflegeheims ein, das Sie bearbeiten möchten: ")
    if care_home_name not in care_homes:
        print(f"Pflegeheim '{care_home_name}' existiert nicht.")
        return
    beds_dict = care_homes[care_home_name]["Bettliste"]
    print(f"Betten Status für '{care_home_name}':")
    for bed_number, occupant in beds_dict.items():
        status = "Belegt" if occupant else "Frei"
        print(f"  - Bett {bed_number}: {status}")
    bed_number = int(input("Bitte geben Sie die Nummer des Bettes ein, das Sie bearbeiten möchten: "))
    if bed_number not in beds_dict:
        print(f"Bett {bed_number} existiert nicht.")
        return
    if beds_dict[bed_number]:
        print(f"Bett {bed_number} ist derzeit belegt von '{beds_dict[bed_number]}'.")
        choice = input("Möchten Sie den Bewohner entfernen? (ja/nein): ").lower()
        if choice in ["j", "y", "ja", "yes"]:
            beds_dict[bed_number] = ""
            print(f"Bett {bed_number} wurde erfolgreich freigegeben.")
    else:
        name_of_occupant = input("Bitte geben Sie den Namen des neuen Bewohners ein: ")
        beds_dict[bed_number] = name_of_occupant
        print(f"Bett {bed_number} wurde erfolgreich mit '{name_of_occupant}' belegt.")

def name_care_home():
    name = input("Bitte geben Sie den Namen des Pflegeheims ein: ")
    return name

def create_care_home():
    name = name_care_home()
    if name in care_homes:
        print("Ein Pflegeheim mit diesem Namen existiert bereits. Bitte wählen Sie einen anderen Namen.")
        return
    print("Wie viele Betten soll das neue Pflegeheim haben?")
    print("1: 50 Betten")
    print("2: 75 Betten")
    print("3: 100 Betten")
    choice = input("Wählen Sie eine Option: ")
    if choice in ["1", "50"]:
        beds = 50
        beds_dict = {i+1: "" for i in range(beds)}
    elif choice in ["2", "75"]:
        beds = 75
        beds_dict = {i+1: "" for i in range(beds)}
    elif choice in ["3", "100"]:
        beds = 100
        beds_dict = {i+1: "" for i in range(beds)}  # Empty string means the bed is free
    else:
        print("Ungültige Option. Bitte wählen Sie 1, 2 oder 3.")
        return
    care_homes[name] = {"Betten": beds, "Bettliste": beds_dict}
    print(f"Pflegeheim '{name}' mit {beds} Betten wurde erfolgreich angelegt.")

def print_header(title):
    print("\n" + "=" * 50)
    print(f" {title.upper()}")
    print("=" * 50)

def main():
    while True:
        print_header("Hauptmenü")
        #print(care_homes)
        print("1: Auskunft über angelegte Daten")
        print("2: Pflegeheim anpassen")
        print("3: Pflegeheim anlegen")
        option = input("Wählen Sie eine Option: ")

        if option == "1":
            info()
        elif option == "2":
            edit_care_home()
        elif option == "3":
            create_care_home()
        else:
            print("Lass dir ruhig Zeit, du musst nicht sofort eine Option wählen. Bitte wähle eine der angegebenen Optionen.")

if __name__ == "__main__":
    main()
