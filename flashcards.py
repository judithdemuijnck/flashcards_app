import datetime
import sqlite3
import termcolor
import tkinter as tk

testing_vocabulary = []
entire_vocabulary = []
chosen_vocabulary = []


class Flashcard:
    def __init__(self, term, translation, last_accessed,
                 created, level_num, language):
        self.term = term
        self.translation = translation
        self.last_accessed = last_accessed
        self.created = created
        self.level_num = level_num
        self.language = language

    def add_to_database(self):
        connection = sqlite3.connect("vocabulary_new.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS entire_vocabulary
            (term TEXT, 
            translation TEXT, 
            last_accessed TEXT, 
            created TEXT, 
            level_num INTEGER, 
            language TEXT);""")
        cursor.execute("INSERT INTO entire_vocabulary VALUES (?,?,?,?,?,?)",
                       (self.term,
                        self.translation,
                        self.last_accessed,
                        self.created,
                        self.level_num,
                        self.language))
        connection.commit()
        connection.close()


class DataBase:
    def __init__(self):
        self.load_db()
        self.languages = self.grab_all_languages()

    def load_db(self):
        connection = sqlite3.connect("vocabulary_new.db")
        cursor = connection.cursor()
        # check vocabulary is not empty
        vocabulary_exists = list(cursor.execute(
            """SELECT name
            FROM sqlite_schema
            WHERE type='table'
            AND name='entire_vocabulary';"""))
        if vocabulary_exists:
            db_reader = cursor.execute("""SELECT * 
                                        FROM entire_vocabulary;""")
            for row in db_reader:
                vocab = Flashcard(row[0], row[1], row[2],
                                  row[3], row[4], row[5])
                entire_vocabulary.append(vocab)
        connection.commit()
        connection.close()

    def saving(self):
        connection = sqlite3.connect("vocabulary_new.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS entire_vocabulary 
                (term TEXT, 
                translation TEXT, 
                last_accessed TEXT, 
                created TEXT, 
                level_num INTEGER, 
                language TEXT);""")
        cursor.execute("DELETE FROM entire_vocabulary;")
        insert_query = "INSERT INTO entire_vocabulary VALUES (?,?,?,?,?,?);"
        for vocab in entire_vocabulary:
            cursor.execute(insert_query, (vocab.term,
                                          vocab.translation,
                                          vocab.last_accessed,
                                          vocab.created,
                                          vocab.level_num,
                                          vocab.language))
        connection.commit()
        connection.close()

    def grab_all_languages(self):
        languages = []
        for vocab in entire_vocabulary:
            if vocab.language not in languages:
                languages.append(vocab.language)
        return languages


class Vocabulary:

    def __init__(self, language):
        self.language = language
        self.select_vocabulary()

        now = datetime.datetime.now()
        now_timestamp = datetime.datetime.timestamp(now)
        # create individual levels
        self.level_1 = self._create_level(1, 0, now_timestamp)
        self.level_2 = self._create_level(2,
                                          (86400 * 3), now_timestamp)
        self.level_3 = self._create_level(
            3, 604800, now_timestamp)
        self.level_4 = self._create_level(4,
                                          (604800*2), now_timestamp)
        self.level_5 = self._create_level(
            5, 2629743, now_timestamp)
        self.level_6 = self._create_level(6, 0, 0)

    def select_vocabulary(self):
        for vocab in entire_vocabulary:
            if vocab.language == self.language:
                chosen_vocabulary.append(vocab)

    def _create_level(self, level, time_to_compare, now):
        level_list = []
        for vocab in chosen_vocabulary:
            if vocab.level_num == level:
                level_list.append(vocab)
                last_accessed = vocab.last_accessed
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) > time_to_compare:
                    testing_vocabulary.append(vocab)
        return level_list

    # def _load_db(self, level_num, time_to_compare, now):

    #         for row in db_reader:
    #             vocab = Flashcard(row[0], row[1], row[2],
    #                               row[3], row[4], row[5])
    #             level.append(vocab)
    #             entire_vocabulary.append(vocab)
    #             last_accessed = vocab.last_accessed
    #             last_accessed = datetime.datetime.fromisoformat(
    #                 last_accessed)
    #             last_accessed = datetime.datetime.timestamp(last_accessed)
    #             if (now - last_accessed) > time_to_compare:
    #                 testing_vocabulary.append(vocab)
    #     connection.commit()
    #     connection.close()
    #     return level

    def level_up(self, random_vocab):
        all_levels = self.make_all_levels()
        done = False
        for idx, level in enumerate(all_levels):
            for item in level:
                if random_vocab.term == item.term \
                        and random_vocab.translation == item.translation:
                    testing_vocabulary.remove(random_vocab)
                    random_vocab.last_accessed = datetime.datetime.now()
                    random_vocab.level_num = random_vocab.level_num + 1
                    all_levels[idx+1].append(random_vocab)
                    level.remove(random_vocab)
                    done = True
                    break
            if done:
                break

    def level_down(self, random_vocab):
        all_levels = self.make_all_levels()
        all_levels.remove(self.level_1)
        done = False
        for level in all_levels:
            for item in level:
                if random_vocab.term == item.term \
                        and random_vocab.translation == item.translation:
                    random_vocab.last_accessed = datetime.datetime.now()
                    random_vocab.level_num = 1
                    level.remove(random_vocab)
                    self.level_1.append(random_vocab)
                    done = True
                    break
            if done:
                break

    def check_if_vocab_already_exists(self, term=None, translation=None):
        already_exists = False
        for vocab in chosen_vocabulary:
            if term == vocab.term or \
                    translation == vocab.translation:
                already_exists = True
        return already_exists

    def make_all_levels(self):
        all_levels = all_levels = [self.level_1, self.level_2,
                                   self.level_3, self.level_4,
                                   self.level_5, self.level_6]
        return all_levels

    # def not_empty(self):
    #     all_levels = self.make_all_levels()
    #     not_empty = False
    #     for level in all_levels:
    #         if level:
    #             not_empty = True
    #     return not_empty


db = DataBase()


class ScrollbarFrame(tk.Frame):
    """
    Extends class tk.Frame to support a scrollable Frame
    This class is independent from the widgets to be scrolled and
    can be used to replace a standard tk.Frame
    """

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        # The Scrollbar, layout to the right
        vsb = tk.Scrollbar(self, orient="vertical")
        vsb.pack(side="right", fill="y")

        # The Canvas which supports the Scrollbar Interface, layout to the left
        self.canvas = tk.Canvas(self, borderwidth=0)  # background="#ffffff"
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind the Scrollbar to the self.canvas Scrollbar Interface
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.configure(command=self.canvas.yview)

        # The Frame to be scrolled, layout into the canvas
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = tk.Frame(
            self.canvas)  # background=self.canvas.cget('bg')
        self.canvas.create_window(
            (10, 10), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
