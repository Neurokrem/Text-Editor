import os
from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import *
from tkinter.filedialog import *


def colour_change():
    colour = colorchooser.askcolor(title="Choose your colour")
    text_area.config(fg=colour[1])


def font_change(*args):
    text_area.config(font=(font_name.get(), frame_size.get()))


def new_file():
    window.title("No title")
    text_area.delete(1.0, END)


def open_file():
    file = askopenfilename(defaultextension=".txt",
                               filetypes=[("All files", "*.*"),
                                          ("Text", ".txt"),
                                          ("HTML", ".html"),
                                          ("PDF", ".pdf")])
    try:
        window.title(os.path.basename(file))
        text_area.delete(1.0, END)

        file = open(file, "r")
        text_area.insert(1.0, file.read())
    except Exception:
        print("Cannot be read")

    finally:
        file.close()


def save():
    file = filedialog.asksaveasfilename(initialfile="Unnamed.txt",
                                            defaultextension=".txt",
                                            filetypes=[("All files", "*.*"),
                                                       ("Text", ".txt"),
                                                       ("HTML", ".html"),
                                                       ("PDF", ".pdf")])
    if file is None:
        return
    else:
        try:
            window.title(os.path.basename(file))
            file = open(file, "w")

            file.write(text_area.get(1.0, END))

        except Exception:
            print("Not possible to save")

        finally:
            file.close()


def copy():
    text_area.event_generate("<<Copy>>")


def cut():
    text_area.event_generate("<<Cut>>")


def paste():
    text_area.event_generate("<<Paste>>")


def about():
    showinfo("About", "This program was made by Igor Vidanović, February 2022")


def izlaz():
    window.destroy()


window = Tk()
window.title("Editor")

# file definition
file = None

# Constants
window_width = 500
window_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))


window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

font_name = StringVar(window)
font_name.set("Arial")

font_size = StringVar(window)
font_size.set("25")

text_area = Text(window, font=(font_name.get(), font_size.get()))

# Scroll definition
scroller = Scrollbar(text_area)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
text_area.grid(sticky=N + E + S + W)

frame = Frame(window)
frame.grid()

# Colour, size and other buttons
button_colour = Button(frame, text="Colour", command=colour_change)
button_colour.grid(row=0, column=0)

font_okvir = OptionMenu(frame, font_name, *font.families(), command=font_change)
font_okvir.grid(row=0, column=1)

frame_size = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=font_change)
frame_size.grid(row=0, column=2)

scroller.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scroller.set)

# Main menu at the top
menu = Menu(window)
window.config(menu=menu)

# "File"
file_selection = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_selection)
file_selection.add_command(label="New file", command=new_file)
file_selection.add_command(label="Open file", command=open_file)
file_selection.add_command(label="Save file", command=save)
file_selection.add_separator()
file_selection.add_command(label="Exit", command=izlaz)

# "Edit"
edit_selection = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_selection)
edit_selection.add_command(label="Copy", command=copy)
edit_selection.add_command(label="Paste", command=paste)
edit_selection.add_command(label="Cut", command=cut)

# "Help"
help_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

window.mainloop()
