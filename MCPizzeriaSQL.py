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

def maakNieuweTabellen():
    # Maak een nieuwe tabel met 3 kolommen: id, naam, prijs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_pizzas(
            gerechtID INTEGER PRIMARY KEY AUTOINCREMENT,
            gerechtNaam TEXT NOT NULL,
            gerechtPrijs REAL NOT NULL);""")
    print("Tabel 'tbl_pizzas' aangemaakt.")


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_klanten(
        klantNr INTEGER PRIMARY KEY AUTOINCREMENT,
        klantAchternaam TEXT);""")
    print("Tabel 'tbl_klanten' aangemaakt.")


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_winkelWagen(
        bestelRegel INTEGER PRIMARY KEY AUTOINCREMENT,
        klantNr INTEGER,
        gerechtID INTEGER,
        aantal INTEGER NOT NULL,
        FOREIGN KEY (klantNr) REFERENCES tbl_klanten(klantNr)
        FOREIGN KEY (gerechtID) REFERENCES tbl_pizzas(gerechtID)
        );""")
    print("Tabel 'tbl_winkelWagen' aangemaakt.")

    #db.commit() # update de database


def printTabel(tabel_naam):
    cursor.execute("SELECT * FROM " + tabel_naam) #SQL om ALLE gegevens te halen
    opgehaalde_gegevens = cursor.fetchall() #sla gegevens op in een variabele
    print("Tabel " + tabel_naam + ":", opgehaalde_gegevens) #druk gegevens af


def voegKlantenToe():
    cursor.execute("INSERT INTO tbl_klanten VALUES(NULL, ?)", ("Janssen",))
    cursor.execute("INSERT INTO tbl_klanten VALUES(NULL, ?)", ("Smit",))
    printTabel("tbl_klanten")
    #db.commit() #gegevens naar de database wegschrijven

def voegPizzasToe():
    cursor.execute("INSERT INTO tbl_pizzas VALUES(NULL, ?, ? )", ("Hawaii", 12.25))
    cursor.execute("INSERT INTO tbl_pizzas VALUES(NULL, ?, ? )", ("Salami", 10.00))
    printTabel("tbl_pizzas")
   # db.commit() #gegevens naar de database wegschrijven


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


def vraagOpGegevensPizzaTabel():
    cursor.execute("SELECT * FROM tbl_pizzas")
    resultaat = cursor.fetchall()
    print("Tabel tbl_pizzas:", resultaat)
    return resultaat

#Zoek alle gegevens over pizza met ingevoerde naam
def zoekPizza(ingevoerde_pizzanaam):
    cursor.execute("SELECT * FROM tbl_pizzas WHERE gerechtNaam = ?", ( ingevoerde_pizzanaam, ) )
    zoek_resultaat = cursor.fetchall()
    if zoek_resultaat == []: #resultaat is leeg, geen gerecht gevonden
        print("Helaas, geen match gevonden met "+ ingevoerde_pizzanaam)
    else:
        print("Pizza gevonden: ", zoek_resultaat )
    return zoek_resultaat

def voegToeAanWinkelWagen(klantNr, gerechtID, aantal):
    cursor.execute("INSERT INTO tbl_winkelWagen VALUES(NULL, ?, ?, ?)", (klantNr, gerechtID, aantal,))
    db.commit() #gegevens naar de database wegschrijven
    printTabel("tbl_winkelWagen")


def vraagOpGegevensWinkelWagenTabel():
    cursor.execute("SELECT * FROM tbl_winkelWagen")
    resultaat = cursor.fetchall()
    print("Tabel tbl_winkelWagen:", resultaat)
    return resultaat


### --------- Hoofdprogramma  ----------------
maakNieuweTabellen()
#voegPizzasToe()
#voegKlantenToe()


