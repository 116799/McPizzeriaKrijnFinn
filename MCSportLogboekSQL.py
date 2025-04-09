# Vul hier de naam van je programma in:
# MCPizzeria
#
# Vul hier jullie namen in:
# Finn Mooiman en Krijn Meulenkamp
#
#

### --------- Bibliotheken en globale variabelen -----------------
import sqlite3
with sqlite3.connect("MCPizzeria.db") as db:
    #cursor is object waarmee je data uit de database kan halen
    cursor = db.cursor()




### ---------  Functie definities  -----------------
#reset de tabellen
cursor.execute("DROP TABLE IF EXISTS tbl_oefeningen")

def maakNieuweTabellen():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_oefeningen(
            oefeningID INTEGER PRIMARY KEY AUTOINCREMENT,
            Oefening TEXT NOT NULL,
            Spiergroep TEXT);""")
    print("Tabel 'tbl_oefeningen' aangemaakt.")


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_klanten(
        klantNr INTEGER PRIMARY KEY AUTOINCREMENT,
        klantAchternaam TEXT);""")
    print("Tabel 'tbl_klanten' aangemaakt.")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_Logboek(
        logboekRegel INTEGER PRIMARY KEY AUTOINCREMENT,
        klantNr INTEGER,
        oefeningID INTEGER,
        aantal INTEGER NOT NULL,
        gewicht REAL,
        FOREIGN KEY (klantNr) REFERENCES tbl_klanten(klantNr),
        FOREIGN KEY (oefeningID) REFERENCES tbl_oefeningen(oefeningID));""")
    print("Tabel 'tbl_Logboek' aangemaakt.")

    try:
        cursor.execute("ALTER TABLE tbl_Logboek ADD COLUMN datum TEXT")
    except sqlite3.OperationalError:
        pass

    db.commit() # update de database


def printTabel(tabel_naam):
    cursor.execute("SELECT * FROM " + tabel_naam) #SQL om ALLE gegevens te halen
    opgehaalde_gegevens = cursor.fetchall() #sla gegevens op in een variabele
    print("Tabel " + tabel_naam + ":", opgehaalde_gegevens) #druk gegevens af


def voegKlantenToe():
    klanten = ["Janssen", "Smit"]
    for achternaam in klanten:
        cursor.execute("SELECT * FROM tbl_klanten WHERE klantAchternaam = ?", (achternaam,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO tbl_klanten VALUES(NULL, ?)", (achternaam,))
    db.commit()
    printTabel("tbl_klanten")


def voegOefeningenToe():
    oefeningen = [
        ("Bench Press", "Borst"),
        ("Leg Press", "Benen")
        ]
    for oefening, spiergroep in oefeningen:
        cursor.execute("SELECT * FROM tbl_oefeningen WHERE Oefening = ?", (oefening,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO tbl_oefeningen VALUES(NULL, ?, ?)", (oefening, spiergroep))
    db.commit()
    printTabel("tbl_oefeningen")



#Zoek alle gegevens over klant met ingevoerde naam
def zoekKlantInTabel(ingevoerde_klantnaam):
    cursor.execute("SELECT * FROM tbl_klanten WHERE klantAchternaam = ?", (ingevoerde_klantnaam,))
    zoek_resultaat = cursor.fetchall()

    if zoek_resultaat == []: #resultaat is leeg, geen gerecht gevonden
        print("Geen klant gevonden met achternaam", ingevoerde_klantnaam)
        print("Klant wordt nu toegevoegd.")
        cursor.execute("INSERT INTO tbl_klanten VALUES(NULL, ? )", (ingevoerde_klantnaam, ))
        db.commit() #gegevens naar de database wegschrijven

        print("Klant toegevoegd aan 'tbl_klanten':" + ingevoerde_klantnaam  )
        printTabel("tbl_klanten")

        #nu dat klant in tabel is gezet, kunnen we zijn gegevens ophalen
        cursor.execute("SELECT * FROM tbl_klanten WHERE klantAchternaam = ?",(ingevoerde_klantnaam,))
        zoek_resultaat = cursor.fetchall()

    return zoek_resultaat


def vraagOpGegevensOefeningenTabel():
    cursor.execute("SELECT * FROM tbl_oefeningen")
    resultaat = cursor.fetchall()
    print("Tabel tbl_oefeningen:", resultaat)
    return resultaat

#Zoek alle gegevens over pizza met ingevoerde naam
def zoekOefening(ingevoerde_oefeningnaam):
    cursor.execute("SELECT * FROM tbl_oefeningen WHERE Oefening = ?", ( ingevoerde_oefeningnaam, ) )
    zoek_resultaat = cursor.fetchall()
    if zoek_resultaat == []: #resultaat is leeg, geen gerecht gevonden
        print("Helaas, geen match gevonden met "+ ingevoerde_oefeningnaam)
    else:
        print("Oefening gevonden: ", zoek_resultaat )
    return zoek_resultaat

def voegToeAanLogboek(klantNr, oefeningID, aantal, gewicht, datum):
    cursor.execute("INSERT INTO tbl_Logboek VALUES(NULL, ?, ?, ?, ?, ?)", (klantNr, oefeningID, aantal, gewicht, datum))
    db.commit() #gegevens naar de database wegschrijven


def vraagOpGegevensLogboekTabel():
    cursor.execute("SELECT * FROM tbl_Logboek")
    resultaat = cursor.fetchall()
    print("Tabel tbl_Logboek:", resultaat)
    return resultaat

def geefLogboekVoorKlant(klantNr):
    cursor.execute("""
        SELECT tbl_Logboek.logboekRegel, tbl_oefeningen.Oefening, tbl_Logboek.aantal, tbl_Logboek.gewicht, tbl_Logboek.datum
        FROM tbl_Logboek
        JOIN tbl_oefeningen ON tbl_Logboek.oefeningID = tbl_oefeningen.oefeningID
        WHERE tbl_Logboek.klantNr = ?
    """, (klantNr,))
    return cursor.fetchall()



### --------- Hoofdprogramma  ----------------
maakNieuweTabellen()
voegOefeningenToe()
voegKlantenToe()