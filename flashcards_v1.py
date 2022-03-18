import random
import termcolor
import datetime
import csv
import flashcards

level_1 = []  # every day # 86400 seconds unix time stamp
level_2 = []  # every 3 days # 86400 * 3
level_3 = []  # every week 604800 seconds unix time stamp
level_4 = []  # every 2 weeks 604800*2
level_5 = []  # every month 2629743 seconds unix time stamp
level_6 = []  # long-term memory, never, #final

testing_vocabulary = []


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
    for idx, level in enumerate(vocabulary):
        print(termcolor.colored(f"Level {idx+1}", attrs=["bold"]))
        for vocab in level:
            print(vocab.term, "|", vocab.translation, "|",
                  vocab.last_accessed, "|", vocab.created)
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
        for item in level:
            if make_changes in item.term:
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
                term, translation = vocab.split(": ")
            except ValueError:
                print(
                    "Sorry, something went wrong. Did you follow the guidelines? Try again!")
            else:
                vocabulary = [level_1, level_2,
                              level_3, level_4, level_5, level_6]
                already_exists = False
                for level in vocabulary:
                    for item in level:
                        if term in item.term:
                            already_exists = True
                if already_exists:
                    print(f"Sorry, {term} is already in your vocabulary. You can update your vocabulary. Go to vocabulary now? y/n")
                    make_changes = input()
                    if make_changes == "y":
                        access_vocabulary()
                        exit()
                    else:
                        print("Okay, get ready to create your next term.")
                else:
                    vocab = flashcards.Flashcard(
                        term, translation, datetime.datetime.now(), datetime.datetime.now())
                    level_1.append(vocab)
                    testing_vocabulary.append(vocab)
                    with open("level_1.csv", "a") as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerow(
                            [term, translation, datetime.datetime.now(), datetime.datetime.now()])
                    cont = input(
                        "Done! Term saved to vocabulary! Keep going? y/n: ")
    menu()


def practising_vocabulary():
    reverse = False
    print("Would you like to practise with a reversed vocabulary? Type 'r' to reverse or 'n' for no.")
    should_reverse = input()

    if should_reverse.casefold() == "r" or should_reverse.casefold() == "y":
        reverse = True

    while testing_vocabulary:
        random_vocab = random.choice(testing_vocabulary)
        if reverse:
            practice(random_vocab.translation, random_vocab.term, random_vocab)
        else:
            practice(random_vocab.term, random_vocab.translation, random_vocab)
    print("Well done, you've completed your vocabulary!")
    menu()


def practice(question, check_against, random_vocab):
    print(f"What is the translation of '{question}'?")
    answer = input()
    if answer == check_against:
        print(termcolor.colored(answer, "green"))
        print(f"Correct! Leveling up '{check_against}'!")
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
        print(f"Sorry, the correct answer is '{check_against}'. Would you like to level up anyway? y/n")
        answer = input()
        if answer == "y":
            print(f"Okay, leveling up {check_against}")
            level_up(random_vocab)
        else:
            print(f"{check_against} will be moved back to level 1.")
            level_down(random_vocab)


def check_if_vocab_empty(testing_vocabulary):
    if testing_vocabulary:
        practising_vocabulary()
    else:
        print("Well done, you've completed your vocabulary!")
        menu()


def level_up(random_vocab):
    vocabulary = [level_1, level_2, level_3, level_4, level_5, level_6]
    done = False
    for idx, level in enumerate(vocabulary):
        for item in level:
            if random_vocab.term == item.term and random_vocab.translation == item.translation:
                testing_vocabulary.remove(random_vocab)
                random_vocab.last_accessed = datetime.datetime.now()
                vocabulary[idx+1].append(random_vocab)
                level.remove(random_vocab)
                done = True
                break
        if done:
            break


def level_down(random_vocab):
    vocabulary = [level_2, level_3, level_4, level_5, level_6]
    done = False
    for level in vocabulary:
        for item in level:
            if random_vocab.term == item.term and random_vocab.translation == item.translation:
                level_1.append(random_vocab)
                level.remove(random_vocab)
                done = True
                break
        if done:
            break


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
                vocab = flashcards.Flashcard(row[0], row[1], row[2], row[3])
                level_1.append(vocab)
                testing_vocabulary.append(vocab)
    except FileNotFoundError:
        pass

    try:
        with open("level_2.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                vocab = flashcards.Flashcard(row[0], row[1], row[2], row[3])
                level_2.append(vocab)
                last_accessed = vocab.last_accessed
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) >= (86400 * 3):
                    testing_vocabulary.append(vocab)
    except FileNotFoundError:
        pass

    try:
        with open("level_3.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                vocab = flashcards.Flashcard(row[0], row[1], row[2], row[3])
                level_3.append(vocab)
                last_accessed = vocab.last_accessed
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) >= 604800:
                    testing_vocabulary.append(row)
    except FileNotFoundError:
        pass

    try:
        with open("level_4.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                vocab = flashcards.Flashcard(row[0], row[1], row[2], row[3])
                level_4.append(vocab)
                last_accessed = vocab.last_accessed
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) >= (604800*2):
                    testing_vocabulary.append(vocab)
    except FileNotFoundError:
        pass

    try:
        with open("level_5.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                vocab = flashcards.Flashcard(row[0], row[1], row[2], row[3])
                level_5.append(vocab)
                last_accessed = vocab.last_accessed
                last_accessed = datetime.datetime.fromisoformat(last_accessed)
                last_accessed = datetime.datetime.timestamp(last_accessed)
                if (now - last_accessed) >= 2629743:
                    testing_vocabulary.append(vocab)
    except FileNotFoundError:
        pass

    try:
        with open("level_6.csv") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                vocab = flashcards.Flashcard(row[0], row[1], row[2], row[3])
                level_6.append(vocab)
    except FileNotFoundError:
        pass


def saving():
    with open("level_1.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_1:
            csv_writer.writerow(
                [vocab.term, vocab.translation, vocab.last_accessed, vocab.created])

    with open("level_2.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_2:
            csv_writer.writerow(
                [vocab.term, vocab.translation, vocab.last_accessed, vocab.created])

    with open("level_3.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_3:
            csv_writer.writerow(
                [vocab.term, vocab.translation, vocab.last_accessed, vocab.created])

    with open("level_4.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_4:
            csv_writer.writerow(
                [vocab.term, vocab.translation, vocab.last_accessed, vocab.created])

    with open("level_5.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_5:
            csv_writer.writerow(
                [vocab.term, vocab.translation, vocab.last_accessed, vocab.created])

    with open("level_6.csv", "w") as file:
        csv_writer = csv.writer(file)
        for vocab in level_6:
            csv_writer.writerow(
                [vocab.term, vocab.translation, vocab.last_accessed, vocab.created])


loading_vocabulary()

menu()


# TO DO

# how do i deal with headers? no header atm


# level_1 = {"term": "translation",
#            "Guten Morgen": "Goedemorgen", "ihr": "jullie"}

### LEVEL UP IF I WANTED TO MAKE DATABASE WORK WITH DICTS ###
# def level_up(random vocab):
#     if random_vocab in level_1 or random_vocab in level_1.values():
#         if random_vocab in level_1:
#             level_2[random_vocab] = level_1[random_vocab]
#             level_1.pop(random_vocab)
#         else:
#             reversed_back = reverse_back(random_vocab, level_1)
#             level_2[reversed_back] = level_1[reversed_back]
#             level_1.pop(reversed_back)
#         with open("level_1.csv") as file:
#             csv_reader = list(csv.reader(file))

#         with open("level_1.csv", "w") as file:
#             csv_writer = csv.writer(file)
#             for line in csv_reader:
#                 print("yes")
#                 if random_vocab in line:
#                     temp_random_vocab = line
#                 else:
#                     csv_writer.writerow(line)
#         temp_random_vocab[2] = datetime.datetime.now()
#         with open("level_2.csv", "a") as file:
#             csv_writer = csv.writer(file)
#             csv_writer.writerow(temp_random_vocab)
