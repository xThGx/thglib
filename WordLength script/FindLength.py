while True:
    text = input("Geben Sie ein Wort ein: ")

    # Abbruchbedingung prüfen
    if text.lower() in ["q", "b", "e", "x"]:
        print("Programm beendet.")
        break

    print(f"Die Länge des Wortes beträgt {len(text)} Zeichen.\n")