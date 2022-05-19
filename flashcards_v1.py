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
create_new_vocabulary_var = "Create new vocabulary"
#### ----------------------- #####


def save_quit():
    flashcards.db.saving()
    window.quit()


def practising_vocabulary():
    practice_top = gui_practice_vocabulary.PracticeVocabulary(vocabulary)
    practice_top.geometry("1000x600")
    practice_top.title("Flashcards | Practice")


def creating_vocabulary():
    create_top = gui_create_vocabulary.CreateVocabulary(vocabulary)
    create_top.geometry("1000x600")
    create_top.title("Flashcards | Create Vocabulary")


def access_vocabulary():
    vocabulary_top = gui_access_vocabulary.PrintVocabulary(vocabulary)
    vocabulary_top.geometry("1000x600")
    vocabulary_top.title("Flashcards | Your Vocabulary")


def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def show_menu(language):
    global vocabulary
    vocabulary = flashcards.Vocabulary(language)

    # create LOGO
    image = Image.open("Flashcards_logo.png")
    logo = ImageTk.PhotoImage(image)
    logo_lbl = tk.Label(master=window, image=logo, width=1000, bg=logo_bg)
    logo_lbl.image = logo

    # empty label as filler
    empty_lbl = tk.Label(master=window, width=111, height=5)
    menu_frame = tk.Frame(master=window, width=1000, height=480, bg=logo_bg)

    # language_lbl = tk.Label(master=menu_frame)

    language_lbl = tk.Label(
        master=menu_frame, text=language, font=("Poppins", 20))

    # BUTTONS
    quit_btn = tk.Button(master=menu_frame,
                         text="Quit",
                         font=("Poppins", 15),
                         highlightbackground=logo_bg,
                         fg=logo_chip,
                         height=2,
                         width=20,
                         command=window.quit)
    practice_btn = tk.Button(master=menu_frame,
                             text="Practice Vocabulary",
                             font=("Poppins", 15),
                             highlightbackground=logo_bg,
                             fg=logo_chip,
                             height=2,
                             width=20,
                             command=practising_vocabulary)
    access_btn = tk.Button(master=menu_frame,
                           text="Access Vocabulary",
                           font=("Poppins", 15),
                           highlightbackground=logo_bg,
                           fg=logo_chip,
                           height=2,
                           width=20,
                           command=access_vocabulary)
    create_btn = tk.Button(master=menu_frame,
                           text="Add to Vocabulary",
                           font=("Poppins", 15),
                           highlightbackground=logo_bg,
                           fg=logo_chip,
                           height=2,
                           width=20,
                           command=creating_vocabulary)

    # PLACEMENT of WIDGETS

    logo_lbl.grid(columnspan=4, row=0, column=0)
    empty_lbl.grid(columnspan=4, row=1, column=0)
    menu_frame.grid(columnspan=4, rowspan=3, row=2, column=0)
    language_lbl.grid(columnspan=2, row=2, column=1)
    quit_btn.grid(row=3, column=1)
    practice_btn.grid(row=3, column=2)
    access_btn.grid(row=4, column=1)
    create_btn.grid(row=4, column=2)


def create_menu(event):
    language = event.widget["text"]
    clear_window()
    if language == create_new_vocabulary_var:
        create_new_vocabulary()
    else:
        show_menu(language)


def submit_vocabulary(event):
    language = new_vocabulary_entry.get()
    show_menu(language)


def create_new_vocabulary():
    # create LOGO
    image = Image.open("Flashcards_logo.png")
    logo = ImageTk.PhotoImage(image)
    logo_lbl = tk.Label(master=window, image=logo,
                        width=1000, bg=logo_bg)
    logo_lbl.image = logo

    # empty label as filler
    empty_lbl = tk.Label(master=window,
                         width=111, height=5)
    new_vocabulary_frame = tk.Frame(
        master=window, width=1000, height=480, bg=logo_bg)
    new_vocabulary_lbl = tk.Label(master=new_vocabulary_frame,
                                  text="What is your new vocabulary called?",
                                  font=("Poppins", 20))

    global new_vocabulary_entry
    new_vocabulary_entry = tk.Entry(master=new_vocabulary_frame,
                                    font=("Poppins", 15))
    new_vocabulary_entry.bind("<Return>", submit_vocabulary)
    new_vocabulary_entry.focus()
    new_vocabulary_submit_btn = tk.Button(master=new_vocabulary_frame,
                                          text="Create Vocabulary",
                                          font=("Poppins", 15))
    new_vocabulary_submit_btn.bind("<Button-1>", submit_vocabulary)

    # PLACEMENT of WIDGETS
    logo_lbl.grid(columnspan=4, row=0, column=0)
    empty_lbl.grid(columnspan=4, row=1, column=0)
    new_vocabulary_frame.grid(columnspan=4, rowspan=3, row=2, column=0)
    new_vocabulary_lbl.grid(row=2, column=0)
    new_vocabulary_entry.grid(row=3, column=0)
    new_vocabulary_submit_btn.grid(row=4, column=0)


## START GUI ##
window = tk.Tk()
window.geometry("1000x600")
window.title("Flashcards")

# create LOGO
image = Image.open("Flashcards_logo.png")
logo = ImageTk.PhotoImage(image)
logo_lbl = tk.Label(master=window, image=logo, width=1000, bg=logo_bg)
logo_lbl.image = logo


# empty label as filler
empty_lbl = tk.Label(master=window, width=111, height=5)
choice_frame = tk.Frame(master=window, width=1000, height=480, bg=logo_bg)

# WHICH VOCABULARY
choose_label = tk.Label(master=choice_frame,
                        text="Which vocabulary do you want to access?",
                        font=("Poppins", 20))

row_num = 3

for language in flashcards.db.languages:
    language_btn = tk.Button(master=choice_frame,
                             text=language,
                             font=("Poppins", 20))
    language_btn.grid(row=row_num, column=0)
    language_btn.bind("<Button-1>", create_menu)
    row_num += 1

create_btn = tk.Button(master=choice_frame,
                       text=create_new_vocabulary_var,
                       font=("Poppins", 20))
create_btn.grid(row=row_num, column=0)
create_btn.bind("<Button-1>", create_menu)
# tk.Button(master=menu_frame, text="START",
#           command=show_menu).grid(row=3, column=0)

# PLACEMENT of WIDGETS
logo_lbl.grid(columnspan=4, row=0, column=0)
empty_lbl.grid(columnspan=4, row=1, column=0)
choice_frame.grid(columnspan=4, rowspan=(
    len(flashcards.db.languages)+1), row=2, column=0)
choose_label.grid(row=2, column=0)


window.mainloop()

flashcards.db.saving()


# TO DO
# go over search bar (make sure you can use backspace as well, use ANY key)


# CHOSE VOCABULARY


# pull types of vocabulary (dutch, italian), put in a list
# ask which vocabulary you want to use (dutch, italian, etc...)
# or create a new one
# if new, give name to new vocabulary, go straight to create_vocabulary
# save with name in vocabulary.db
# else
# only pull entrys with chosen vocabulary from vocabulary.db
#


# feed vocabular yobject into tkinter classes to make it accessible
