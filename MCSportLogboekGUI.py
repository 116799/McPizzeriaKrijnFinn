# Vul hier de naam van je programma in:
# MCPizzeria
#
# Vul hier jullie namen in:
# Finn Mooiman en Krijn Meulenkamp
#
#

### --------- Bibliotheken en globale variabelen -----------------
from tkinter import *
import MCSportLogboekSQL




### --------- Functie definities  ----------------------

def zoekKlant():
    #haal de ingevoerde_klantnaam op uit het invoerveld
    #     en gebruik dit om met SQL de klant in database te vinden
    gevonden_klanten = MCSportLogboekSQL.zoekKlantInTabel(ingevoerde_klantnaam.get())

    invoerveldKlantnaam.delete(0, END)
    invoerveldKlantNr.delete(0, END)
    invoerveldGeselecteerdeOefening.delete(0, END)
    listboxLogboek.delete(0, END)

    ingevoerd_gewicht.set(0)
    aantalGeslecteerdeHerhalingen.set(0)

    listboxOefeningen.delete(0, END)
    listboxOefeningen.insert(0, "ID\tOefening\tSpiergroep")
    oefeningen = MCSportLogboekSQL.vraagOpGegevensOefeningenTabel()
    for regel in oefeningen:
        listboxOefeningen.insert(END, regel)

    for rij in gevonden_klanten: 
        invoerveldKlantNr.insert(END, rij[0])
        invoerveldKlantnaam.insert(END, rij[1])

    if gevonden_klanten:
        klantNr = gevonden_klanten[0][0]
        logboek_gegevens = MCSportLogboekSQL.geefLogboekVoorKlant(klantNr)
        listboxLogboek.insert(0, "Datum\tOefening\tHerhalingen\tGewicht")
        for regel in logboek_gegevens:
            _, oefening, aantal, gewicht, datum = regel
            listboxLogboek.insert (END, f"{datum}{oefening}{aantal}{gewicht} kg")


def toonOefeningenInListbox():
    listboxOefeningen.delete(0, END)  #maak de listbox leeg
    listboxOefeningen.insert(0, "ID\tOefening\tSpiergroep")
    Oefeningen_tabel = MCSportLogboekSQL.vraagOpGegevensOefeningenTabel()
    for regel in Oefeningen_tabel:
        listboxOefeningen.insert(END, regel) #voeg elke regel uit resultaat in listboxMenu


### functie voor het selecteren van een rij uit de listbox en deze in een andere veld te plaatsen
def haalGeselecteerdeRijOp(event):
    #bepaal op welke regel er geklikt is
    geselecteerdeRegelInLijst = listboxOefeningen.curselection()[0]
    #haal tekst uit die regel
    geselecteerdeTekst = listboxOefeningen.get(geselecteerdeRegelInLijst)
    #verwijder tekst uit veld waar je in wilt schrijven, voor het geval er al iets staat
    invoerveldGeselecteerdeOefening.delete(0, END)
    #zet tekst in veld
    invoerveldGeselecteerdeOefening.insert(0, geselecteerdeTekst)



def voegToeAanLogboek():
    klantNr = invoerveldKlantNr.get()
    oefening_string = geselecteerdeOefening.get()
    if not oefening_string:
        print("Selecteer eerst een oefening.")
        return
    
    try:
        oefeningID = int(oefening_string.split()[0])  # eerste getal uit string
    except ValueError:
        print("Fout bij het ophalen van oefeningID.")
        return

    aantalSets = aantalGeslecteerdeHerhalingen.get()
    Gewicht = float(ingevoerd_gewicht.get())
    if not ValueError:
        print("Ongeldig gewicht")
        return

    from datetime import date, datetime

    datum_input = ingevoerde_datum.get().strip()

    # Als het veld leeg is gebruik vandaag
    if datum_input == "":
        datum = date.today().isoformat()
    else:
        try:
            ingevoerde_datum_obj = datetime.strptime(datum_input, "%Y-%m-%d").date()
            vandaag = date.today()

            if ingevoerde_datum_obj > vandaag:
                print("Je kunt geen datum in de toekomst invullen.")
                return  # Stop de functie, sla niets op

            datum = ingevoerde_datum_obj.isoformat()  # Correcte datum, opslaan

        except ValueError:
            print("Ongeldige datum. Gebruik formaat: JJJJ-MM-DD (bijv. 2024-04-18).") 
            return  # Stop de functie als de datum ongeldig is


    MCSportLogboekSQL.voegToeAanLogboek(klantNr, oefeningID, aantalSets, Gewicht, datum)
    
    listboxLogboek.delete(0, END)
    logboek_gegevens = MCSportLogboekSQL.geefLogboekVoorKlant(klantNr)
    listboxLogboek.insert(0, "Oefening\tHerhalingen\tGewicht (kg)")
    for regel in logboek_gegevens:
        _, oefening, aantal, gewicht, datum = regel
        listboxLogboek.insert(END, f"{datum}\t{oefening}\t{aantal}\t{gewicht} kg")


### --------- Hoofdprogramma  ----------------
venster = Tk()
venster.wm_title("MC Sport Database")
venster.iconbitmap("MC_icon.ico")
venster.config(bg="lightblue")

labelIntro = Label(venster, text="Welkom!")
labelIntro.grid(row=0, column=0, sticky="E", padx=10, pady=5)


labelKlantnaam = Label(venster, text="Klantnaam")
labelKlantnaam.grid(row=1, column=0, sticky="W")

ingevoerde_klantnaam = StringVar()
invoerveldKlantnaam = Entry(venster, textvariable=ingevoerde_klantnaam)
invoerveldKlantnaam.grid(row=1, column=1, sticky="W")


labelKlantnr = Label(venster, text="Klantnummer")
labelKlantnr.grid(row=2, column=0, sticky="W")

invoerveldKlantNr = Entry(venster)
invoerveldKlantNr.grid(row=2, column=1, sticky="W")


knopZoekOpKlantnaam = Button(venster, text="Zoek klant", width=12, command=zoekKlant)
knopZoekOpKlantnaam.grid(row=1, column=4)


labellistboxOefeningen = Label(venster, text="Mogelijkheden:")
labellistboxOefeningen.grid(row=5, column=0, sticky="W")# sticky="W" zorgt dat tekst links uitgelijnd wordt

listboxOefeningen = Listbox(venster, height=6, width=45)
listboxOefeningen.grid(row=5, column=1, rowspan=6, columnspan=2, sticky="W")
listboxOefeningen.bind('<<ListboxSelect>>', haalGeselecteerdeRijOp)


scrollbarlistboxOefeningen = Scrollbar(venster)
scrollbarlistboxOefeningen.grid(row=4, column=2, rowspan=6, sticky="E")
listboxOefeningen.config(yscrollcommand=scrollbarlistboxOefeningen.set)
scrollbarlistboxOefeningen.config(command=listboxOefeningen.yview)

knopToonAlleOefeningen = Button(venster, text="Toon alle oefeningen", width=12, command=toonOefeningenInListbox)
knopToonAlleOefeningen.grid(row=5, column=4)

labelinvoerveldSelecteerdeOefening = Label(venster, text="Gekozen Oefening:")
labelinvoerveldSelecteerdeOefening.grid(row=11, column=0, sticky="W")

geselecteerdeOefening= StringVar()
invoerveldGeselecteerdeOefening = Entry(venster, textvariable=geselecteerdeOefening)
invoerveldGeselecteerdeOefening.grid(row=11, column=1, columnspan=2, sticky="W")

ingevoerde_datum = StringVar()
labelDatum = Label(venster, text="Datum (YYYY-MM-DD):")
labelDatum.grid(row=14, column=0, sticky="W")

invoerveldDatum = Entry(venster, textvariable=ingevoerde_datum)
invoerveldDatum.grid(row=14, column=1, columnspan=2, sticky="w")


### KIES AANTAL VAN DE GESELECTEERDE PIZZA
labelAantalHerhalingenGeselecteerd = Label(venster, text="Aantal herhalingen:")
labelAantalHerhalingenGeselecteerd.grid(row=13, column=0, sticky="W")

labelGewichtGeselecteerd = Label(venster, text="Gewicht (Kg):")
labelGewichtGeselecteerd.grid(row=13, column=1, sticky="E")

ingevoerd_gewicht = StringVar()
invoerveldGewicht = Entry(venster, textvariable=ingevoerd_gewicht)
invoerveldGewicht.grid(row=13, column=2, sticky="w")

aantalGeslecteerdeHerhalingen = IntVar() #het is een getal
aantalGeslecteerdeHerhalingen.set(0) #eerste standaard waarde
optionMenuHerhalingenAantal = OptionMenu(venster, aantalGeslecteerdeHerhalingen, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40)
optionMenuHerhalingenAantal.grid(row=13, column=1, sticky="W")

knopVoegToeAanLogboek = Button(venster, text="Voeg toe", width=12, command=voegToeAanLogboek)
knopVoegToeAanLogboek.grid(row=13, column=4)


labellistboxLogboek = Label(venster, text="logboek:")
labellistboxLogboek.grid(row=15, column=0, sticky="W")

listboxLogboek = Listbox(venster, height=6, width=45)
listboxLogboek.grid(row=15, column=1, rowspan=4, columnspan=2, sticky="W")

scrollbarlistboxLogboek = Scrollbar(venster)
scrollbarlistboxLogboek.grid(row=16, column=2, rowspan=4, sticky="E")
listboxLogboek.config(yscrollcommand=scrollbarlistboxLogboek.set)
scrollbarlistboxLogboek.config(command=listboxLogboek.yview)

knopSluit = Button(venster, text="Sluiten",width=12,command=venster.destroy)
knopSluit.grid(row=18, column = 4)


#reageert op gebruikersinvoer, deze regel als laatste laten staan
venster.mainloop()