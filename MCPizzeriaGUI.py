# Vul hier de naam van je programma in:
# MCPizzeria
#
# Vul hier jullie namen in:
# Finn Mooiman en Krijn Meulenkamp
#
#

### --------- Bibliotheken en globale variabelen -----------------
from tkinter import *
import MCPizzeriaSQL


### --------- Functie definities  ----------------------

def zoekKlant():
    #haal de ingevoerde_klantnaam op uit het invoerveld
    #     en gebruik dit om met SQL de klant in database te vinden
    gevonden_klanten = MCPizzeriaSQL.zoekKlantInTabel(ingevoerde_klantnaam.get())

    print(gevonden_klanten) # om te testen
    invoerveldKlantnaam.delete(0, END)  #invoerveld voor naam leeg maken
    invoerveldKlantNr.delete(0, END)  #invoerveld voor klantNr leeg maken

    for rij in gevonden_klanten: #voor elke rij dat de query oplevert
        #toon klantnummer, de eerste kolom uit het resultaat in de invoerveld
        invoerveldKlantNr.insert(END, rij[0])

        #toon klantAchternaam, de tweede kolom uit het resultaat in de invoerveld
        invoerveldKlantnaam.insert(END, rij[1])


#optionele opdracht:
def zoekPizza():
    listboxMenu.delete(0, END)  # maak de listbox voor de zekerheid leeg
    listboxMenu.insert(0, "ID \t Gerecht \t \t Prijs") #print de kolomnamen af

    #haal de ingevoerde_pizzanaam op
    #     en gebruik dit om met SQL gerecht in database te vinden
    # gezochte_pizzas = MCPizzeriaSQL.zoekPizza( ingevoerde_pizzanaam.get() )
    # for rij in gezochte_pizzas: #voor elke rij dat de query oplevert
    #     listboxMenu.insert(END, rij) #toon die rij in de listbox


def toonMenuInListbox():
    listboxMenu.delete(0, END)  #maak de listbox leeg
    listboxMenu.insert(0, "ID \t Gerecht \t \t Prijs")
    pizza_tabel = MCPizzeriaSQL.vraagOpGegevensPizzaTabel()
    for regel in pizza_tabel:
        listboxMenu.insert(END, regel) #voeg elke regel uit resultaat in listboxMenu


### functie voor het selecteren van een rij uit de listbox en deze in een andere veld te plaatsen
def haalGeselecteerdeRijOp(event):
    #bepaal op welke regel er geklikt is
    geselecteerdeRegelInLijst = listboxMenu.curselection()[0]
    #haal tekst uit die regel
    geselecteerdeTekst = listboxMenu.get(geselecteerdeRegelInLijst)
    #verwijder tekst uit veld waar je in wilt schrijven, voor het geval er al iets staat
    invoerveldGeselecteerdeOefening.delete(0, END)
    #zet tekst in veld
    invoerveldGeselecteerdeOefening.insert(0, geselecteerdeTekst)


#voeg de bestelling van klant met gekozen pizza en aantal toe
#in de winkelwagentabel
#en toon de bestelling in de listbox op het scherm
def voegToeAanLogboek():
    klantNr = invoerveldKlantNr.get()
    gerechtID = geselecteerdeOefening.get()
    aantalSets = aantalGeslecteerdeSets.get()
    Gewicht = aantalGewicht.get()

    MCPizzeriaSQL.voegToeAanLogboek(klantNr, gerechtID, aantalSets, Gewicht )

    Logboek_tabel = MCPizzeriaSQL.vraagOpGegevensLogboekTabel()

    listboxLogboek.delete(0, END) #listbox eerst even leeg maken

    for regel in Logboek_tabel:
        listboxLogboek.insert(END, regel)



### --------- Hoofdprogramma  ----------------
venster = Tk()
venster.wm_title("MC Pizzeria")
#venster.iconbitmap("MC_icon.ico")
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




knopZoekOpPizzaNaam = Button(venster, text="Zoek pizza", width=12, command=zoekPizza)
knopZoekOpPizzaNaam.grid(row=3, column=4)


labellistboxMenu = Label(venster, text="Mogelijkheden:")
labellistboxMenu.grid(row=4, column=0, sticky="W")# sticky="W" zorgt dat tekst links uitgelijnd wordt

listboxMenu = Listbox(venster, height=6, width=45)
listboxMenu.grid(row=4, column=1, rowspan=6, columnspan=2, sticky="W")
listboxMenu.bind('<<ListboxSelect>>', haalGeselecteerdeRijOp)


scrollbarlistboxMenu = Scrollbar(venster)
scrollbarlistboxMenu.grid(row=4, column=2, rowspan=6, sticky="E")
listboxMenu.config(yscrollcommand=scrollbarlistboxMenu.set)
scrollbarlistboxMenu.config(command=listboxMenu.yview)

knopToonPizzas = Button(venster, text="Toon alle pizza's", width=12, command=toonMenuInListbox)
knopToonPizzas.grid(row=4, column=4)

labelinvoerveldSelecteerdeOefening = Label(venster, text="Gekozen Oefening:")
labelinvoerveldSelecteerdeOefening.grid(row=11, column=0, sticky="W")

geselecteerdeOefening= StringVar()
invoerveldGeselecteerdeOefening = Entry(venster, textvariable=geselecteerdeOefening)
invoerveldGeselecteerdeOefening.grid(row=11, column=1, columnspan=2, sticky="W")


### KIES AANTAL VAN DE GESELECTEERDE PIZZA
labelAantalSetsGeselecteerd = Label(venster, text="Aantal:")
labelAantalSetsGeselecteerd.grid(row=13, column=0, sticky="W")

labelGewichtGeselecteerd = Label(venster, text="Gewicht (Kg):")
labelGewichtGeselecteerd.grid(row=13, column=1, sticky="W")

aantalGewicht = IntVar() #het is een getal
aantalGewicht.set(1) #eerste standaard waarde
optionMenuGewichtAantal = OptionMenu(venster, aantalGewicht, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80)
optionMenuGewichtAantal.grid(row=14, column=1, sticky="n")

aantalGeslecteerdeSets = IntVar() #het is een getal
aantalGeslecteerdeSets.set(1) #eerste standaard waarde
optionMenuSetsAantal = OptionMenu(venster, aantalGeslecteerdeSets, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)
optionMenuSetsAantal.grid(row=13, column=0, sticky="E")

knopVoegToeAanLogboek = Button(venster, text="Voeg toe", width=12, command=voegToeAanLogboek)
knopVoegToeAanLogboek.grid(row=13, column=4)


labellistboxLogboek = Label(venster, text="logboek:")
labellistboxLogboek.grid(row=15, column=0, sticky="W")# zorgt dat tekst links uitgelijnd wordt


listboxLogboek = Listbox(venster, height=6, width=45)
listboxLogboek.grid(row=15, column=1, rowspan=4, columnspan=2, sticky="W")
listboxLogboek.bind('<<ListboxSelect>>')

knopSluit = Button(venster, text="Sluiten",width=12,command=venster.destroy)
knopSluit.grid(row=18, column = 4)


# fotoPad = "fotoPepperoni.png"
#
# padFotoGeselecteerdePizza = PhotoImage(file=fotoPad)
# fotoPizza = Label(venster, width=100, height=100, image=padFotoGeselecteerdePizza)
# fotoPizza.grid(row=18, column=0, columnspan=2, sticky="W")


#reageert op gebruikersinvoer, deze regel als laatste laten staan
venster.mainloop()
