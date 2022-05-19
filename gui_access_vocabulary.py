import tkinter as tk
import flashcards
from PIL import Image, ImageTk
import datetime

#### VARIABLES, COLOURS, ETC #####
logo_bg = "#b0eedb"
logo_chip = "#137DC5"
logo_font = "Avenir Next Pro Light"


class PrintVocabulary(tk.Toplevel):
    def __init__(self, vocabulary):
        super().__init__()
        self.vocabulary = vocabulary

        sbf = flashcards.ScrollbarFrame(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        sbf.grid(row=0, column=0, sticky='nsew')
        global frame
        frame = sbf.scrolled_frame

        # create LOGO
        image = Image.open("Flashcards_logo.png")
        logo = ImageTk.PhotoImage(image)
        logo_lbl = tk.Label(master=frame, image=logo, width=1000, bg=logo_bg)
        logo_lbl.image = logo

        top_logo_lbl = tk.Label(master=frame,
                                image=logo, width=1000, bg=logo_bg)
        top_logo_lbl.grid(columnspan=5, row=0, column=0)

        # create DELETE icon
        delete_img = Image.open("delete_icon.png")
        global delete_icon
        delete_icon = ImageTk.PhotoImage(delete_img)

        # Display vocabulary

        row_num = 2

        # make sure vocabulary not empt
        if flashcards.chosen_vocabulary:
            global all_levels
            all_levels = self.vocabulary.make_all_levels()
            for idx, level in enumerate(all_levels):
                self.create_title(f"Level {idx+1}", row_num)
                row_num += 1
                for item in level:
                    self.create_vocabulary_entry(item, row_num)
                    row_num += 1

            menu_btn = tk.Button(
                master=frame, text="Back to Menu", command=self.destroy)
            menu_btn.grid(row=1, column=0)
            quit_btn = tk.Button(
                master=frame, text="Save & Quit", command=self.quit)
            quit_btn.grid(row=1, column=1)
        else:
            tk.Label(master=frame,
                     text="Your vocabulary is empty.",
                     font=("Poppins", 20)).grid(row=row_num, column=0)

        # Search Bar
        global search_entry
        search_entry = tk.Entry(master=frame, fg="LightGray")
        search_entry.insert(tk.END, "Search...")
        search_entry.grid(row=1, column=4)
        global clicked_search_bar
        clicked_search_bar = search_entry.bind(
            "<Button-1>", self.clear_search_bar)
        search_entry.bind("<Return>", self.search_vocabulary)

        global widget_list
        widget_list = all_children(self)

    def clear_search_bar(self, event):
        search_entry.delete(0, tk.END)
        search_entry["fg"] = "Black"
        search_entry.unbind("<Button-1>", clicked_search_bar)

    def search_vocabulary(self, event):

        search_term = search_entry.get()

        for item in widget_list[6:-3:]:
            item.grid_remove()

        row_num = 2
        for level in all_levels:
            for item in level:
                if search_term in item.term or search_term in item.translation:
                    self.create_vocabulary_entry(item, row_num)
                    row_num += 1

    def create_title(self, level_num, row_num):
        tk.Label(master=frame,
                 text=level_num,
                 font=("Poppins", 15, "bold"),
                 width=100,
                 height=1,
                 bg=logo_chip,
                 relief=tk.SOLID).grid(
            columnspan=5,
            row=row_num,
            column=0,
            pady=1)

    def create_vocabulary_entry(self, item, row_num):
        delete_btn = tk.Button(
            master=frame,
            image=delete_icon)
        delete_btn.image = delete_icon
        delete_btn.bind("<Double-Button-1>", self.delete_vocabulary)
        delete_btn.grid(row=row_num, column=0)
        term_lbl = tk.Label(master=frame,
                            text=item.term,
                            width=20,
                            height=1,
                            font=("Poppins", 12),
                            bg=logo_bg)
        term_lbl.grid(row=row_num, column=1)
        term_lbl.bind("<Double-Button-1>", self.make_changes)
        translation_lbl = tk.Label(master=frame,
                                   text=item.translation,
                                   width=20,
                                   height=1,
                                   bg=logo_bg,
                                   font=("Poppins", 12))
        translation_lbl.grid(row=row_num, column=2)
        translation_lbl.bind("<Double-Button-1>", self.make_changes)
        if isinstance(item.last_accessed, str):
            last_accessed = datetime.datetime.fromisoformat(
                item.last_accessed)
        else:
            last_accessed = item.last_accessed
        last_accessed_lbl = tk.Label(master=frame,
                                     text=last_accessed.strftime(
                                         "%c"),
                                     bg=logo_bg,
                                     width=20,
                                     height=1,
                                     font=("Poppins", 12))
        last_accessed_lbl.grid(row=row_num, column=3)
        if isinstance(item.created, str):
            created = datetime.datetime.fromisoformat(item.created)
        else:
            created = item.created
        created_lbl = tk.Label(master=frame,
                               text=created.strftime("%c"),
                               bg=logo_bg,
                               width=20,
                               height=1,
                               font=("Poppins", 12))
        created_lbl.grid(row=row_num, column=4)

    def reverse_search(self):
        pass

    def make_changes(self, event):
        global text_to_change
        text_to_change = event.widget["text"]
        global widget_row
        widget_row = event.widget.grid_info()["row"]
        global widget_column
        widget_column = event.widget.grid_info()["column"]
        event.widget.grid_forget()

        global changes_entry
        changes_entry = tk.Entry(master=frame)
        changes_entry.insert(0, text_to_change)
        changes_entry.grid(row=widget_row, column=widget_column)
        changes_entry.bind("<Return>", self.submit_change)

    def submit_change(self, event):
        global changed_text
        changed_text = changes_entry.get()
        if self.vocabulary.check_if_vocab_already_exists(
                changed_text, changed_text):
            changes_entry["fg"] = "red"
        else:
            for level in all_levels:
                for item in level:
                    if widget_column == 1:
                        if item.term == text_to_change:
                            item.term = changed_text
                            self.submit_change_to_testing_vocabulary(
                                text_to_change, changed_text)
                            break
                    elif widget_column == 2:
                        if item.translation == text_to_change:
                            item.translation = changed_text
                            self.submit_change_to_testing_vocabulary(
                                text_to_change, changed_text)
                            break
            changes_entry.destroy()
            changed_text_lbl = tk.Label(
                master=frame,
                text=changed_text,
                bg=logo_bg,
                width=20,
                height=1,
                font=("Poppins", 12))
            changed_text_lbl.bind("<Double-Button-1>", self.make_changes)
            changed_text_lbl.grid(row=widget_row, column=widget_column)

    def submit_change_to_testing_vocabulary(
            self, text_to_change, changed_text):
        for item in flashcards.testing_vocabulary:
            if widget_column == 1:
                if item.term == text_to_change:
                    item.term = changed_text
                    break
            elif widget_column == 2:
                if item.translation == text_to_change:
                    item.translation = changed_text
                    break

    def delete_vocabulary(self, event):

        event_row = event.widget.grid_info()["row"]
        term_to_be_deleted = frame.grid_slaves(
            row=event_row, column=1)[0]
        translation_to_be_deleted = frame.grid_slaves(
            row=event_row, column=2)[0]

        # REMOVE from all_levels
        for level in all_levels:
            for item in level:
                if item.term == term_to_be_deleted["text"] \
                        and \
                        item.translation == translation_to_be_deleted["text"]:
                    level.remove(item)
                    flashcards.entire_vocabulary.remove(item)
                    flashcards.chosen_vocabulary.remove(item)
                    if item in flashcards.testing_vocabulary:
                        flashcards.testing_vocabulary.remove(item)

        for column_num in range(5):
            frame.grid_slaves(row=event_row, column=column_num)[0].destroy()


def all_children(root):
    _list = root.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list
