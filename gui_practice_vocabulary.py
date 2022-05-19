import tkinter as tk
import flashcards
from PIL import Image, ImageTk
import random

#### VARIABLES, COLOURS, ETC #####
logo_bg = "#b0eedb"
logo_chip = "#137DC5"
logo_font = "Avenir Next Pro Light"


class PracticeVocabulary(tk.Toplevel):

    def __init__(self, vocabulary):
        super().__init__()
        self.create_window()
        self.vocabulary = vocabulary
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

    def create_window(self):

        # create LOGO
        image = Image.open("Flashcards_logo.png")
        logo = ImageTk.PhotoImage(image)
        logo_lbl = tk.Label(master=self, image=logo, width=1000, bg=logo_bg)
        logo_lbl.image = logo

        top_logo_lbl = tk.Label(master=self,
                                image=logo, width=1000, bg=logo_bg)

        # container
        frame_a = tk.Frame(master=self, height=480,
                           width=500, pady=10)
        frame_b = tk.Frame(master=self, height=480,
                           width=500, padx=20, pady=10)
        frame_c = tk.Frame(master=self, height=240, width=1000,
                           borderwidth=5, padx=10, pady=10)

        lbl_frame_a = tk.LabelFrame(
            master=frame_a, bg=logo_chip,
            relief=tk.RIDGE, borderwidth=5,
            padx=10, pady=10)
        lbl_frame_b = tk.LabelFrame(
            master=frame_b, bg=logo_chip,
            relief=tk.RIDGE, borderwidth=5,
            padx=10, pady=10)
        lbl_frame_c = tk.LabelFrame(
            master=frame_c, bg=logo_chip,
            relief=tk.RIDGE, borderwidth=5,
            padx=10, pady=10)

        # CREATE WIDGETS
        global question_lbl
        question_lbl = tk.Label(master=lbl_frame_a, font=(
            "Poppins", 15), height=8, width=30, relief=tk.RIDGE)
        global answer_txt
        answer_txt = tk.Text(master=lbl_frame_b, font=(
            "Poppins", 15), height=10, width=34, relief=tk.RIDGE)
        global check_answer_btn
        check_answer_btn = tk.Button(
            master=frame_b, text="Check Your Answer")
        global reverse
        reverse = tk.IntVar()
        reverse_checkbtn = tk.Checkbutton(master=frame_a,
                                          text="""Train with
                                          reversed vocabulary?""",
                                          variable=reverse,
                                          onvalue=1, offvalue=0,
                                          command=self._start_loop)

        global terminal_lbl
        terminal_lbl = tk.Label(master=lbl_frame_c,
                                text="This will show action",
                                font=("Poppins", 12),
                                height=5, width=60,
                                relief=tk.RIDGE)

        # BIND BUTTONS to FUNCTIONS
        menu_btn = tk.Button(master=frame_b, text="Return to Menu",
                             command=self.destroy)
        quit_btn = tk.Button(
            master=frame_b, text="Save & Quit", command=self.quit)
        answer_txt.bind("<Return>", self._check_answer)
        check_answer_btn.bind("<Button-1>", self._check_answer)

        # ACTION

        if flashcards.testing_vocabulary:
            self._start_loop()
        else:
            terminal_lbl["text"] = """Congratulations,
            you have completed your vocabulary!"""
            self.after(2000, self.destroy)

        ## PLACEMENT of WIDGETS ##
        top_logo_lbl.grid(columnspan=4, row=0, column=0)
        frame_a.grid(columnspan=2, rowspan=3, row=1, column=0)
        frame_b.grid(columnspan=2, rowspan=6, row=1, column=2)
        frame_c.grid(row=5, column=0)
        lbl_frame_a.grid(columnspan=2, rowspan=2, row=1, column=0)
        lbl_frame_b.grid(columnspan=2, rowspan=2, row=1, column=2)
        lbl_frame_c.grid(row=5, column=0)
        question_lbl.grid(columnspan=2, rowspan=2, row=1, column=0)
        reverse_checkbtn.grid(row=3, column=0)
        answer_txt.grid(columnspan=2, rowspan=2, row=1, column=2)
        check_answer_btn.grid(row=3, column=2)
        terminal_lbl.grid(row=5, column=0)
        menu_btn.grid(row=4, column=2)
        quit_btn.grid(row=4, column=3)

    def _start_loop(self):
        global random_vocab
        random_vocab = random.choice(flashcards.testing_vocabulary)
        global question
        question = ""
        global check_against
        check_against = ""
        if reverse.get() == 1:
            question = random_vocab.translation
            check_against = random_vocab.term
        else:
            question = random_vocab.term
            check_against = random_vocab.translation
        question_lbl["text"] = question
        terminal_lbl["text"] = f"""What is the translation of 
                        '{question}'?"""

    def _check_answer(self, event):
        answer = answer_txt.get("1.0", "end-1c")
        check_answer_btn["text"] = "Continue"
        check_answer_btn.bind("<Button-1>", self._continue_loop)
        answer_txt.bind("<Return>", self._continue_loop)
        if answer == check_against or answer == f"\n{check_against}":
            answer_txt["fg"] = "green"
            terminal_lbl["text"] = f"Correct! \nLeveling up '{answer}'."
            self.vocabulary.level_up(random_vocab)
        else:
            answer_txt["fg"] = "red"
            terminal_lbl["text"] = f"""'{answer}' is wrong. 
            The correct answer is '{check_against}'.\n 
            '{check_against}' will be moved back to level 1."""
            self.vocabulary.level_down(random_vocab)
            answer_txt.after(3000, self.delete_answer)

    def _continue_loop(self, event):
        answer_txt["fg"] = "black"
        if flashcards.testing_vocabulary:
            self._start_loop()
            answer_txt.delete("1.0", tk.END)
            check_answer_btn["text"] = "Check your answer"
            check_answer_btn.bind("<Button-1>", self._check_answer)
            answer_txt.bind("<Return>", self._check_answer)
        else:
            terminal_lbl["text"] = """Congratulations, 
            you have completed your vocabulary!"""
            flashcards.db.saving()
            self.after(2000, self.destroy)

    def delete_answer(self):
        answer_txt.delete("1.0", tk.END)
