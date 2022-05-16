import tkinter as tk
import flashcards
from PIL import Image, ImageTk
import datetime

#### VARIABLES, COLOURS, ETC #####
logo_bg = "#b0eedb"
logo_chip = "#137DC5"
logo_font = "Avenir Next Pro Light"


class CreateVocabulary(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.create_window()

    def create_window(self):
        # create LOGO
        image = Image.open("Flashcards_logo.png")
        logo = ImageTk.PhotoImage(image)
        logo_lbl = tk.Label(master=self, image=logo, width=1000, bg=logo_bg)
        logo_lbl.image = logo

        top_logo_lbl = tk.Label(master=self,
                                image=logo, width=1000, bg=logo_bg)

        # empty label as filler
        empty_lbl = tk.Label(master=self, width=111, height=3, bg=logo_chip)

        global term_entry
        term_entry = tk.Entry(master=self,
                              font=("Poppins", 12))
        global translation_entry
        translation_entry = tk.Entry(master=self)
        submit_btn = tk.Button(
            master=self, text="Submit")
        menu_btn = tk.Button(
            master=self, text="Back to Menu", command=self.destroy)
        quit_btn = tk.Button(
            master=self, text="Save & Quit", command=self.quit)
        global confirm_lbl
        confirm_lbl = tk.Label(master=self)

        translation_entry.bind("<Return>", _create_vocabulary)
        submit_btn.bind("<Button-1>", _create_vocabulary)

        ## PLACEMENT of WIDGETS ##
        top_logo_lbl.grid(columnspan=5, row=0, column=0)
        empty_lbl.grid(columnspan=5, row=1, column=0)
        term_entry.grid(row=2, column=0)
        translation_entry.grid(row=2, column=1)
        submit_btn.grid(row=2, column=2)
        menu_btn.grid(row=3, column=2)
        quit_btn.grid(row=3, column=3)
        confirm_lbl.grid(row=4, column=0)


def _create_vocabulary(event):
    confirm_lbl.grid_remove()
    term = term_entry.get()
    translation = translation_entry.get()
    term_entry.delete(0, tk.END)
    translation_entry.delete(0, tk.END)
    # confirm_lbl = tk.Label(
    #     master=create_top)
    if flashcards.vocabulary.check_if_vocab_already_exists(term, translation):
        confirm_lbl["text"] = f"""Sorry,
        this is already in your vocabulary."""
        confirm_lbl["fg"] = "red"
    else:
        now = datetime.datetime.now()
        vocab = flashcards.Flashcard(term, translation, now, now)
        flashcards.vocabulary.level_1.append(vocab)
        flashcards.testing_vocabulary.append(vocab)
        vocab.add_to_database()
        confirm_lbl["text"] = f"'{translation}' added to your vocabulary."
        confirm_lbl["fg"] = "green"
    confirm_lbl.grid()
