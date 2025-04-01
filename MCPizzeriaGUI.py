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
    gezochte_pizzas = MCPizzeriaSQL.zoekPizza( ingevoerde_pizzanaam.get() )
    for rij in gezochte_pizzas: #voor elke rij dat de query oplevert
        listboxMenu.insert(END, rij) #toon die rij in de listbox


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
    invoerveldGeselecteerdePizza.delete(0, END)
    #zet tekst in veld
    invoerveldGeselecteerdePizza.insert(0, geselecteerdeTekst)


#voeg de bestelling van klant met gekozen pizza en aantal toe
#in de winkelwagentabel
#en toon de bestelling in de listbox op het scherm
def voegToeAanWinkelWagen():
    klantNr = invoerveldKlantNr.get()
    gerechtID = geselecteerdePizza.get()
    aantal = aantalGeslecteerdePizza.get()

    MCPizzeriaSQL.voegToeAanWinkelWagen(klantNr, gerechtID, aantal )

    winkelwagen_tabel = MCPizzeriaSQL.vraagOpGegevensWinkelWagenTabel()

    listboxWinkelwagen.delete(0, END) #listbox eerst even leeg maken

    for regel in winkelwagen_tabel:
        listboxWinkelwagen.insert(END, regel)



### --------- Hoofdprogramma  ----------------
venster = Tk()
venster.wm_title("MC Pizzeria")
#venster.iconbitmap("MC_icon.ico")
venster.config(bg="skyblue")

labelIntro = Label(venster, text="Welkom!")
labelIntro.grid(row=0, column=0, sticky="W", padx=10, pady=5)


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




labelPizza = Label(venster, text="Pizzanaam:")
labelPizza.grid(row=3, column=0, sticky="W")# sticky="W" zorgt dat tekst links uitgelijnd wordt


ingevoerde_pizzanaam = StringVar()
invoerveldPizzanaam = Entry(venster, textvariable=ingevoerde_pizzanaam)
invoerveldPizzanaam.grid(row=3, column=1, columnspan=2, sticky="W")

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

labelinvoerveldSelecteerdePizza = Label(venster, text="Gekozen pizza:")
labelinvoerveldSelecteerdePizza.grid(row=11, column=0, sticky="W")

geselecteerdePizza= StringVar()
invoerveldGeselecteerdePizza = Entry(venster, textvariable=geselecteerdePizza)
invoerveldGeselecteerdePizza.grid(row=11, column=1, columnspan=2, sticky="W")


### KIES AANTAL VAN DE GESELECTEERDE PIZZA
labelAantalGeselecteerd = Label(venster, text="Aantal:")
labelAantalGeselecteerd.grid(row=12, column=0, sticky="W")

aantalGeslecteerdePizza = IntVar() #het is een getal
aantalGeslecteerdePizza.set(1) #eerste standaard waarde
optionMenuPizzaAantal = OptionMenu(venster, aantalGeslecteerdePizza, 0,1,2,3,4,5,6,7,8)
optionMenuPizzaAantal.grid(row=12, column=1, sticky="W")

knopVoegToeAanWinkelWagen = Button(venster, text="Voeg toe", width=12, command=voegToeAanWinkelWagen)
knopVoegToeAanWinkelWagen.grid(row=12, column=4)


labellistboxWinkelwagen = Label(venster, text="Bestelling:")
labellistboxWinkelwagen.grid(row=13, column=0, sticky="W")# zorgt dat tekst links uitgelijnd wordt


listboxWinkelwagen = Listbox(venster, height=6, width=45)
listboxWinkelwagen.grid(row=13, column=1, rowspan=4, columnspan=2, sticky="W")
listboxWinkelwagen.bind('<<ListboxSelect>>')

knopSluit = Button(venster, text="Sluiten",width=12,command=venster.destroy)
knopSluit.grid(row=17, column = 4)


# fotoPad = "fotoPepperoni.png"
#
# padFotoGeselecteerdePizza = PhotoImage(file=fotoPad)
# fotoPizza = Label(venster, width=100, height=100, image=padFotoGeselecteerdePizza)
# fotoPizza.grid(row=18, column=0, columnspan=2, sticky="W")


#reageert op gebruikersinvoer, deze regel als laatste laten staan
venster.mainloop()
