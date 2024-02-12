import os
from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import *
from tkinter.filedialog import *


# Ovdje definiramo funkcije našeg uređivača teksta
def promjena_boje():
    boja = colorchooser.askcolor(title="Odaberite boju")
    tekst_areal.config(fg=boja[1])


def promjena_fonta(*args):
    tekst_areal.config(font=(ime_fonta.get(), velicina_okvir.get()))


def nova_datoteka():
    # briše sve od početka do krajazahvačenog područja
    # namješta novu datoteku
    prozor.title("Bez naslova")
    tekst_areal.delete(1.0, END)


def otvori_datoteku():
    datoteka = askopenfilename(defaultextension=".txt",
                               filetypes=[("Sve datoteke", "*.*"),
                                          ("Tekst", ".txt"),
                                          ("HTML", ".html"),
                                          ("PDF", ".pdf")])
    try:
        prozor.title(os.path.basename(datoteka))
        tekst_areal.delete(1.0, END)

        datoteka = open(datoteka, "r")
        tekst_areal.insert(1.0, datoteka.read())
    except Exception:
        print("Ne može se učitati")

    finally:
        datoteka.close()


def spremi():
    datoteka = filedialog.asksaveasfilename(initialfile="Neimenovano.txt",
                                            defaultextension=".txt",
                                            filetypes=[("Sve datoteke", "*.*"),
                                                       ("Tekst", ".txt"),
                                                       ("HTML", ".html"),
                                                       ("PDF", ".pdf")])
    if datoteka is None:
        return
    else:
        try:
            prozor.title(os.path.basename(datoteka))
            datoteka = open(datoteka, "w")

            datoteka.write(tekst_areal.get(1.0, END))

        except Exception:
            print("Nije moguće spremiti")

        finally:
            datoteka.close()


def copy():
    tekst_areal.event_generate("<<Copy>>")


def cut():
    tekst_areal.event_generate("<<Cut>>")


def paste():
    tekst_areal.event_generate("<<Paste>>")


def about():
    showinfo("O programu", "Ovaj program je napravio Igor Vidanović, Veljača 2022.")


def izlaz():
    prozor.destroy()


prozor = Tk()
prozor.title("Uređivač")

# definiramo datoteku
datoteka = None

# Konstante
prozor_sirina = 500
prozor_visina = 500
sirina_ekrana = prozor.winfo_screenwidth()
visina_ekrana = prozor.winfo_screenheight()

x = int((sirina_ekrana / 2) - (prozor_sirina / 2))
y = int((visina_ekrana / 2) - (prozor_visina / 2))

# iskreno ne znam zašto smo baš u ovom formatu sastavili sve 4 varijable
# ali funkcionira. tipa Širina x Visina +x +y?
# Inače ovo je dio koji centrira naš početni prozor i daje nam da ga pomičemo, ali ne van
# rubova ekrana.
prozor.geometry("{}x{}+{}+{}".format(prozor_sirina, prozor_visina, x, y))

# postavljamo zadane uvjete pri otvaranju našeg uređivača
ime_fonta = StringVar(prozor)
ime_fonta.set("Arial")

velicina_fonta = StringVar(prozor)
velicina_fonta.set("25")

tekst_areal = Text(prozor, font=(ime_fonta.get(), velicina_fonta.get()))

# Definiramo kliznik
kliznik = Scrollbar(tekst_areal)
prozor.grid_rowconfigure(0, weight=1)
prozor.grid_columnconfigure(0, weight=1)
tekst_areal.grid(sticky=N + E + S + W)

okvir = Frame(prozor)
okvir.grid()

# Gumbi za promjene boje, veličine i vrste fonta
boja_gumb = Button(okvir, text="Boja", command=promjena_boje)
boja_gumb.grid(row=0, column=0)

font_okvir = OptionMenu(okvir, ime_fonta, *font.families(), command=promjena_fonta)
font_okvir.grid(row=0, column=1)

# spinbox je padajuči izbornik veličine
velicina_okvir = Spinbox(okvir, from_=1, to=100, textvariable=velicina_fonta, command=promjena_fonta)
velicina_okvir.grid(row=0, column=2)

kliznik.pack(side=RIGHT, fill=Y)
tekst_areal.config(yscrollcommand=kliznik.set)

# Glavni izbornik pri vrhu
izbornik = Menu(prozor)
prozor.config(menu=izbornik)

# Izbornik "File"
izbornik_datoteke = Menu(izbornik, tearoff=0)
izbornik.add_cascade(label="Datoteka", menu=izbornik_datoteke)
izbornik_datoteke.add_command(label="Nova datoteka", command=nova_datoteka)
izbornik_datoteke.add_command(label="Otvori datoteku", command=otvori_datoteku)
izbornik_datoteke.add_command(label="Spremi datoteku", command=spremi)
izbornik_datoteke.add_separator()
izbornik_datoteke.add_command(label="Izlaz", command=izlaz)

# Izbornik "Edit"
izbornik_uredi = Menu(izbornik, tearoff=0)
izbornik.add_cascade(label="Uredi", menu=izbornik_uredi)
izbornik_uredi.add_command(label="Kopiraj", command=copy)
izbornik_uredi.add_command(label="Zalijepi", command=paste)
izbornik_uredi.add_command(label="Izreži", command=cut)

# Izbornik "Help"

help_menu = Menu(izbornik, tearoff=0)
izbornik.add_cascade(label="Pomoć", menu=help_menu)
help_menu.add_command(label="O programu", command=about)

prozor.mainloop()
