import tkinter as tk
import flashcards
from PIL import Image, ImageTk
import random

#### VARIABLES, COLOURS, ETC #####
logo_bg = "#b0eedb"
logo_chip = "#137DC5"
logo_font = "Avenir Next Pro Light"

done = False


class PracticeVocabulary(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.create_window()
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
        reverse = tk.IntVar()
        reverse_checkbtn = tk.Checkbutton(master=frame_a,
                                          text="""Train with
                                          reversed vocabulary?""",
                                          variable=reverse,
                                          onvalue=1, offvalue=0)

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
        answer_txt.bind("<Return>", _check_answer)
        check_answer_btn.bind("<Button-1>", _check_answer)

        # ACTION

        if flashcards.testing_vocabulary:
            global random_vocab
            random_vocab = random.choice(flashcards.testing_vocabulary)
            question_lbl["text"] = random_vocab.term
            terminal_lbl["text"] = f"What is the \
        	translation of '{random_vocab.term}'?"
            global check_against
            check_against = random_vocab.translation
        else:
            terminal_lbl["text"] = """Congratulations,
        	you have completed your vocabulary!"""
            global done
            done = True
            #self.after(2000, self.destroy)

        #     # if reverse == 1:
        #     #     question_lbl["text"] = random_vocab.translation
        #     # else:
        #     #     question_lbl["text"] = random_vocab.term

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


def _check_answer(event):
    answer = answer_txt.get("1.0", "end-1c")
    check_answer_btn["text"] = "Continue"
    check_answer_btn.bind("<Button-1>", _continue_loop)
    answer_txt.bind("<Return>", _continue_loop)
    if answer == check_against or answer == f"\n{check_against}":
        answer_txt["fg"] = "green"
        terminal_lbl["text"] = f"Correct! \nLeveling up '{answer}'."
        flashcards.vocabulary.level_up(random_vocab)
    else:
        answer_txt["fg"] = "red"
        terminal_lbl["text"] = f"""'{answer}' is wrong. 
        The correct answer is '{check_against}'.\n 
        '{check_against}' will be moved back to level 1."""
        flashcards.vocabulary.level_down(random_vocab)
        answer_txt.after(3000, delete_answer)


def _continue_loop(event):
    answer_txt["fg"] = "black"
    if flashcards.testing_vocabulary:
        global random_vocab
        random_vocab = random.choice(flashcards.testing_vocabulary)
        question_lbl["text"] = random_vocab.term
        global check_against
        check_against = random_vocab.translation
        answer_txt.delete("1.0", tk.END)
        check_answer_btn["text"] = "Check your answer"
        check_answer_btn.bind("<Button-1>", _check_answer)
        answer_txt.bind("<Return>", _check_answer)
    else:
        terminal_lbl["text"] = """Congratulations, 
        you have completed your vocabulary!"""
        flashcards.vocabulary.saving()
        global done
        done = True
        #practice_top.after(2000, practice_top.destroy)


def delete_answer():
    answer_txt.delete("1.0", tk.END)
