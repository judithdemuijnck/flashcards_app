import datetime
import sqlite3
import termcolor

testing_vocabulary = []


class Flashcard:
    def __init__(self, term, translation, last_accessed, created):
        self.term = term
        self.translation = translation
        self.last_accessed = last_accessed
        self.created = created

    def add_to_database(self):
        connection = sqlite3.connect("vocabulary.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS level_1
            (term TEXT, translation TEXT, last_accessed TEXT, created TEXT);""")
        cursor.execute("INSERT INTO level_1 VALUES (?,?,?,?)",
                       (self.term,
                        self.translation, self.last_accessed, self.created))
        connection.commit()
        connection.close()


class Vocabulary:

    def __init__(self):
        now = datetime.datetime.now()
        now_timestamp = datetime.datetime.timestamp(now)
        # initiate db for each table/level
        self.level_1 = self._load_db("level_1", "level_1", 0, now_timestamp)
        self.level_2 = self._load_db("level_2", "level_2",
                                     (86400 * 3), now_timestamp)
        self.level_3 = self._load_db(
            "level_3", "level_3", 604800, now_timestamp)
        self.level_4 = self._load_db("level_4", "level_4",
                                     (604800*2), now_timestamp)
        self.level_5 = self._load_db(
            "level_5", "level_5", 2629743, now_timestamp)
        self.level_6 = self._load_db("level_6", "level_6", 0, 0)

    def _load_db(self, tablename, level, time_to_compare, now):
        level = []
        connection = sqlite3.connect("vocabulary.db")
        cursor = connection.cursor()
        # check if tablename exists
        tablename_exists = list(cursor.execute(
            f"""SELECT name
            FROM sqlite_schema
            WHERE type='table'
            AND name='{tablename}';"""))
        if tablename_exists:
            db_reader = cursor.execute(f"SELECT * FROM {tablename};")
            for row in db_reader:
                vocab = Flashcard(row[0], row[1], row[2], row[3])
                level.append(vocab)
                last_accessed = vocab.last_accessed
                last_accessed = datetime.datetime.fromisoformat(
                    last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) > time_to_compare:
                    testing_vocabulary.append(vocab)
        connection.commit()
        connection.close()
        return level

    def saving(self):
        self._save_db("level_1", self.level_1)
        self._save_db("level_2", self.level_2)
        self._save_db("level_3", self.level_3)
        self._save_db("level_4", self.level_4)
        self. _save_db("level_5", self.level_5)
        self._save_db("level_6", self.level_6)

    def _save_db(self, tablename, level):
        connection = sqlite3.connect("vocabulary.db")
        cursor = connection.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tablename} 
                (term TEXT, translation TEXT, last_accessed TEXT, created TEXT);""")
        cursor.execute(f"DELETE FROM {tablename};")
        insert_query = f"INSERT INTO {tablename} VALUES (?,?,?,?);"
        for vocab in level:
            cursor.execute(insert_query, (vocab.term,
                                          vocab.translation,
                                          vocab.last_accessed,
                                          vocab.created))
        connection.commit()
        connection.close()

    def level_up(self, random_vocab):
        all_levels = self.make_all_levels()
        done = False
        for idx, level in enumerate(all_levels):
            for item in level:
                if random_vocab.term == item.term and random_vocab.translation == item.translation:
                    testing_vocabulary.remove(random_vocab)
                    random_vocab.last_accessed = datetime.datetime.now()
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
                if random_vocab.term == item.term and random_vocab.translation == item.translation:
                    random_vocab.last_accessed = datetime.datetime.now()
                    self.level_1.append(random_vocab)
                    level.remove(random_vocab)
                    done = True
                    break
            if done:
                break

    def check_if_vocab_already_exists(self, term, translation):
        all_levels = self.make_all_levels()
        already_exists = False
        for level in all_levels:
            for item in level:
                if term == item.term:
                    already_exists = True
                elif translation == item.translation:
                    already_exists = True
        return already_exists

    def practice(self, question, check_against, random_vocab):
        print(f"What is the translation of '{question}'?")
        answer = input()
        if answer == check_against:
            print(termcolor.colored(answer, "green"))
            print(f"Correct! Leveling up '{check_against}'!")
            self.level_up(random_vocab)
        elif answer == "q" or answer == "quit":
            print("Okay, quitting the game. See you next time!")
            self.saving()
            quit()
        elif answer == "m" or answer == "menu":
            print("Okay, bringing up the menu.")
            # DOESN'T WORK ATM NEEDS TO BE FIXED
            menu()
            exit()
        else:
            print(termcolor.colored(answer, "red"))
            print(f"Sorry, the correct answer is '{check_against}'. Would you like to level up anyway? y/n")
            answer = input()
            if answer == "y":
                print(f"Okay, leveling up {check_against}")
                self.level_up(random_vocab)
            else:
                print(f"{check_against} will be moved back to level 1.")
                self.level_down(random_vocab)

    def making_changes(self):
        all_levels = self.make_all_levels()
        print("Which term would you like to change?")
        make_changes = input()
        for level in all_levels:
            for item in level:
                if make_changes == item.term:
                    print(
                        "Alright, make your correction like this: 'term: translation/definition'.")
                    vocab = input()
                    try:
                        term, translation = vocab.split(": ")
                    except ValueError:
                        print("Sorry, something went wrong. Try again.")
                    else:
                        item.term = term
                        item.translation = translation
                        item.last_accessed = datetime.datetime.now()
                        print(
                            "Done, changes made! Would you like to make any more changes? y/n")
                        changes = input()
                        return changes
                # elif make_changes == "m":
                #     print("Okay, bringing up menu again.")
                #     # NOT WORKING ATM
                #     menu()
                #     exit()
                elif make_changes == "q" or make_changes == "quit":
                    print("Okay, quitting the game. See you next time!")
                    self.saving()
                    quit()
        print(f"Sorry, couldn't find {make_changes}. Please try again.")
        changes = "y"
        return changes

    def make_all_levels(self):
        all_levels = all_levels = [self.level_1, self.level_2,
                                   self.level_3, self.level_4,
                                   self.level_5, self.level_6]
        return all_levels
