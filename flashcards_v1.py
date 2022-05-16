import random
import termcolor
import datetime
import flashcards
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import gui_practice_vocabulary
import gui_create_vocabulary
import gui_access_vocabulary

#### VARIABLES, COLOURS, ETC #####
logo_bg = "#b0eedb"
logo_chip = "#137DC5"
logo_font = "Avenir Next Pro Light"


def save_quit():
    flashcards.vocabulary.saving()
    window.quit()


def practising_vocabulary():
    practice_top = gui_practice_vocabulary.PracticeVocabulary()
    practice_top.geometry("1000x600")
    practice_top.title("Flashcards | Practice")

    if gui_practice_vocabulary.done:
        practice_top.after(2000, practice_top.destroy)


def creating_vocabulary():
    create_top = gui_create_vocabulary.CreateVocabulary()
    create_top.geometry("1000x600")
    create_top.title("Flashcards | Create Vocabulary")


def access_vocabulary():
    vocabulary_top = gui_access_vocabulary.PrintVocabulary()
    vocabulary_top.geometry("1000x600")
    vocabulary_top.title("Flashcards | Your Vocabulary")


## START GUI ##
window = tk.Tk()
window.geometry("1000x600")
window.title("Flashcards")

# create LOGO
image = Image.open("Flashcards_logo.png")
logo = ImageTk.PhotoImage(image)
logo_lbl = tk.Label(master=window, image=logo, width=1000, bg=logo_bg)
logo_lbl.image = logo

# create EDIT icon
edit_img = Image.open("edit_icon.png")
edit_icon = ImageTk.PhotoImage(edit_img)

# # create DELETE icon
# delete_img = Image.open("delete_icon.png")
# delete_icon = ImageTk. PhotoImage(delete_img)

# empty label as filler
empty_lbl = tk.Label(master=window, width=111, height=3, bg=logo_chip)
menu_frame = tk.Frame(master=window, width=1000, height=480, bg=logo_bg)

# BUTTONS
quit_btn = tk.Button(master=menu_frame, text="Quit", command=window.quit)
practice_btn = tk.Button(
    master=menu_frame,
    text="Practice Vocabulary",
    command=practising_vocabulary)
access_btn = tk.Button(master=menu_frame,
                       text="Access Vocabulary",
                       command=access_vocabulary)
create_btn = tk.Button(master=menu_frame,
                       text="Add to Vocabulary",
                       command=creating_vocabulary)

# PLACEMENT of WIDGETS

logo_lbl.grid(columnspan=4, row=0, column=0)
empty_lbl.grid(columnspan=4, row=1, column=0)
menu_frame.grid(columnspan=4, rowspan=2, row=2, column=0)
quit_btn.grid(row=2, column=1)
practice_btn.grid(row=2, column=2)
access_btn.grid(row=3, column=1)
create_btn.grid(row=3, column=2)


window.mainloop()

flashcards.vocabulary.saving()

# TO DO
# go over search bar (make sure you can use backspace as well, use ANY key)
# reverse practice
# check if vocab already exists when making changes to vocabulary
