import random
import termcolor
import datetime
import csv

level_1 = {}  # every day # 86400 seconds unix time stamp
level_2 = {}  # every 3 days # 86400 * 3
level_3 = {}  # every week 604800 seconds unix time stamp
level_4 = {}  # every 2 weeks 604800*2
level_5 = {}  # every month 2629743 seconds unix time stamp
level_6 = {}  # long-term memory, never, #final

testing_vocabulary = {}


def menu():
    print("What would you like to do?")
    print("To see your existing vocabulary, type 'v'")
    print("To add to your vocabulary, type 'a'")
    print("To start practising your vocabulary, type 'p'")
    print("To quit, type 'q'")
    choices = input()
    choices = choices.casefold()
    if choices == "q":
        print("Okay, quitting the game. See you next time!")
        saving()
        quit()
    elif choices == "v":
        access_vocabulary()
    elif choices == "a":
        creating_vocabulary()
    elif choices == "p":
        practising_vocabulary()
    else:
        print("Sorry, I didn't get that. Try again.")
        menu()


def access_vocabulary():
    global vocabulary
    vocabulary = [level_1, level_2, level_3, level_4, level_5, level_6]
    print("This is your vocabulary: ")
    for idx, item in enumerate(vocabulary):
        print(termcolor.colored(f"Level {idx+1}", attrs=["bold"]))
        for key in item:
            print(key, ":", item[key])
    print("Would you like to make any changes to your existing vocabulary? y/n")
    changes = input()
    while changes == "y":
        changes = making_changes_to_vocabulary()
    print("Okay, bringing up menu again.")
    menu()


def making_changes_to_vocabulary():
    print("Which term would you like to change?")
    make_changes = input()
    for level in vocabulary:
        if make_changes in level:
            level.pop(make_changes)
            print(
                "Alright, make your correction like this: 'term: translation/defintion'.")
            vocab = input()
            try:
                key, value = vocab.split(": ")
            except ValueError:
                print("Sorry, something went wrong. Try again.")
            else:
                level[key] = value
                print("Done, changes made! Would you like to make any more changes? y/n")
                changes = input()
                return changes
        elif make_changes == "m":
            print("Okay, bringing up menu again.")
            menu()
            exit()
        elif make_changes == "q" or make_changes == "quit":
            print("Okay, quitting the game. See you next time!")
            saving()
            quit()
    print(f"Sorry, couldn't find {make_changes}. Please try again.")


def creating_vocabulary():
    cont = "y"
    while cont == "y":
        vocab = input(
            "Please input your term like this: ''term/phrase: translation/definition': ")
        if vocab == "m":
            print("Okay, bringing up menu again.")
            menu()
            exit()
        elif vocab == "q" or vocab == "quit":
            print("Okay, quitting the game. See you next time!")
            saving()
            quit()
        else:
            try:
                key, value = vocab.split(": ")
            except ValueError:
                print(
                    "Sorry, something went wrong. Did you follow the guidelines? Try again!")
            else:
                vocabulary = [level_1, level_2,
                              level_3, level_4, level_5, level_6]
                already_exists = False
                for level in vocabulary:
                    if key in level:
                        already_exists = True
                if already_exists:
                    print(f"Sorry, {key} is already in your vocabulary. You can update your vocabulary. Go to vocabulary now? y/n")
                    make_changes = input()
                    if make_changes == "y":
                        access_vocabulary()
                        exit()
                    else:
                        print("Okay, get ready to create your next term.")
                else:
                    level_1[key] = value
                    testing_vocabulary[key] = value
                    with open("level_1.csv", "a") as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerow(
                            [key, value, datetime.datetime.now()])
                    cont = input(
                        "Done! Term saved to vocabulary! Keep going? y/n: ")
    menu()


def practising_vocabulary():
    # creating dict out of all levels
    # no longer necessary
    global testing_vocabulary
    # testing_vocabulary = {k: v
    #                       for d in (
    #                           level_1, level_2, level_3, level_4, level_5, level_6)
    #                       for k, v in d.items()}

    print("Would you like to practise with a reversed vocabulary? Type 'r' to reverse or 'n' for no.")
    reverse = input()

    if reverse.casefold() == "r" or reverse.casefold() == "y":
        testing_vocabulary = reverse_vocabulary(testing_vocabulary)

    while testing_vocabulary:
        random_vocab = random.choice(list(testing_vocabulary.keys()))
        print(f"What is the translation of '{random_vocab}'?")
        answer = input()
        if answer == testing_vocabulary[random_vocab]:
            print(termcolor.colored(answer, "green"))
            print(f"Correct! Leveling up '{testing_vocabulary[random_vocab]}'!")
            level_up(random_vocab)
        elif answer == "q" or answer == "quit":
            print("Okay, quitting the game. See you next time!")
            saving()
            quit()
        elif answer == "m" or answer == "menu":
            print("Okay, bringing up the menu.")
            menu()
            exit()
        else:
            print(termcolor.colored(answer, "red"))
            print(f"Sorry, the correct answer is '{testing_vocabulary[random_vocab]}'. Would you like to level up anyway? y/n")
            answer = input()
            if answer == "y":
                print(f"Okay, leveling up {testing_vocabulary[random_vocab]}")
                level_up(random_vocab)
            else:
                print(f"{testing_vocabulary[random_vocab]} will be moved back to level 1.")
                level_down(random_vocab)
    print("Well done, you've completed your vocabulary!")
    menu()


def check_if_vocab_empty(testing_vocabulary):
    if testing_vocabulary:
        practising_vocabulary()
    else:
        print("Well done, you've completed your vocabulary!")
        menu()


def level_up(random_vocab):
    vocabulary = [level_1, level_2, level_3, level_4, level_5, level_6]

    for idx, level in enumerate(vocabulary):
        if random_vocab in level:
            vocabulary[idx+1][random_vocab] = level[random_vocab]
            level.pop(random_vocab)
            break
        elif random_vocab in level.values():
            reversed_back = reverse_back(random_vocab, level)
            vocabulary[idx+1][reversed_back] = level[reversed_back]
            level.pop(reversed_back)
            break
    testing_vocabulary.pop(random_vocab)


def level_down(random_vocab):
    vocabulary = [level_2, level_3, level_4, level_5, level_6]
    for level in vocabulary:
        if random_vocab in level:
            level_1[random_vocab] = level[random_vocab]
            level.pop(random_vocab)
        elif random_vocab in level.values():
            reversed_back = reverse_back(random_vocab, level)
            level_1[reversed_back] = level[reversed_back]
            level.pop(reversed_back)


def reverse_vocabulary(testing_vocabulary):
    vocabulary_keys = list(testing_vocabulary.keys())
    vocabulary_values = list(testing_vocabulary.values())
    reversed_vocabulary = {
        vocabulary_values[i]: vocabulary_keys[i] for i in range(len(vocabulary_values))}
    print("Vocabulary revsersed. Starting testing.")
    return reversed_vocabulary


def reverse_back(random_vocab, level):
    return list(level.keys())[list(level.values()).index(random_vocab)]


def loading_vocabulary():
    now = datetime.datetime.now()
    now = datetime.datetime.timestamp(now)
    try:
        with open("level_1.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                level_1[row[0]] = row[1]
                testing_vocabulary[row[0]] = row[1]

    except FileNotFoundError:
        pass

    try:
        with open("level_2.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                level_2[row[0]] = row[1]
                last_accessed = row[2]
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) >= (86400 * 3):
                    testing_vocabulary[row[0]] = row[1]
    except FileNotFoundError:
        pass

    try:
        with open("level_3.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                level_3[row[0]] = row[1]
                last_accessed = row[2]
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) >= 604800:
                    testing_vocabulary[row[0]] = row[1]
    except FileNotFoundError:
        pass

    try:
        with open("level_4.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                level_4[row[0]] = row[1]
                last_accessed = row[2]
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) >= (604800*2):
                    testing_vocabulary[row[0]] = row[1]
    except FileNotFoundError:
        pass

    try:
        with open("level_5.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                level_5[row[0]] = row[1]
                last_accessed = row[2]
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) >= 2629743:
                    testing_vocabulary[row[0]] = row[1]
    except FileNotFoundError:
        pass

    try:
        with open("level_6.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                level_6[row[0]] = row[1]
    except FileNotFoundError:
        pass


def saving():
    with open("level_1.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_1:
            csv_writer.writerow(
                [vocab, level_1[vocab], datetime.datetime.now()])

    with open("level_2.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_2:
            csv_writer.writerow(
                [vocab, level_2[vocab], datetime.datetime.now()])

    with open("level_3.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_3:
            csv_writer.writerow(
                [vocab, level_3[vocab], datetime.datetime.now()])

    with open("level_4.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_4:
            csv_writer.writerow(
                [vocab, level_4[vocab], datetime.datetime.now()])

    with open("level_5.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_5:
            csv_writer.writerow(
                [vocab, level_5[vocab], datetime.datetime.now()])

    with open("level_6.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_6:
            csv_writer.writerow(
                [vocab, level_6[vocab], datetime.datetime.now()])


loading_vocabulary()

menu()


# TO DO
# current problem with saving()
# all same timestamp, even if you haven't practised
# need to save to csv file when it is moved into next level in order to keep original timestamp
# however, how do I do this?
# append to new level and rewrite old level?
# do i have to loop through every line to do that?

# how do i deal with headers? no header atm


# level_1 = {"term": "translation",
#            "Guten Morgen": "Goedemorgen", "ihr": "jullie"}
