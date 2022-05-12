import random
import termcolor
import datetime
import csv
import flashcards
import sqlite3

level_1 = []  # every day # 86400 seconds unix time stamp
level_2 = []  # every 3 days # 86400 * 3
level_3 = []  # every week 604800 seconds unix time stamp
level_4 = []  # every 2 weeks 604800*2
level_5 = []  # every month 2629743 seconds unix time stamp
level_6 = []  # long-term memory, never, #final


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
        vocabulary.saving()
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
    global all_levels
    all_levels = vocabulary.make_all_levels()
    print("This is your vocabulary: ")
    for idx, level in enumerate(all_levels):
        print(termcolor.colored(f"Level {idx+1}", attrs=["bold"]))
        for vocab in level:
            print(vocab.term, "|", vocab.translation, "|",
                  vocab.last_accessed, "|", vocab.created)
    print("Would you like to make any changes to your existing vocabulary? y/n")
    changes = input()
    while changes == "y":
        changes = vocabulary.making_changes()
    print("Okay, bringing up menu again.")
    menu()


def making_changes_to_vocabulary():
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
            elif make_changes == "m":
                print("Okay, bringing up menu again.")
                menu()
                exit()
            elif make_changes == "q" or make_changes == "quit":
                print("Okay, quitting the game. See you next time!")
                vocabulary.saving()
                quit()
        print(f"Sorry, couldn't find {make_changes}. Please try again.")


def creating_vocabulary():
    global cont
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
            vocabulary.saving()
            quit()
        else:
            try:
                term, translation = vocab.split(": ")
            except ValueError:
                print(
                    "Sorry, something went wrong. Did you follow the guidelines? Try again!")
            else:
                if vocabulary.check_if_vocab_already_exists(term, translation) == True:
                    print(f"Sorry, {term} is already in your vocabulary. You can update your vocabulary. Go to vocabulary now? y/n")
                    make_changes = input()
                    if make_changes == "y":
                        access_vocabulary()
                        exit()
                    else:
                        print("Okay, get ready to create your next term.")
                else:
                    now = datetime.datetime.now()
                    vocab = flashcards.Flashcard(term, translation, now, now)
                    vocabulary.level_1.append(vocab)
                    flashcards.testing_vocabulary.append(vocab)
                    cont = input(
                        "Done! Term saved to your vocabulary! Keep going? y/n: ")
    menu()


def practising_vocabulary():
    reverse = False
    print("Would you like to practise with a reversed vocabulary? Type 'r' to reverse or 'n' for no.")
    should_reverse = input()

    if should_reverse.casefold() == "r" or should_reverse.casefold() == "y":
        reverse = True

    while flashcards.testing_vocabulary:
        random_vocab = random.choice(flashcards.testing_vocabulary)
        if reverse:
            vocabulary.practice(random_vocab.translation,
                                random_vocab.term, random_vocab)
        else:
            vocabulary.practice(random_vocab.term,
                                random_vocab.translation, random_vocab)
    print("Well done, you've completed your vocabulary!")
    menu()


def practice(question, check_against, random_vocab):
    print(f"What is the translation of '{question}'?")
    answer = input()
    if answer == check_against:
        print(termcolor.colored(answer, "green"))
        print(f"Correct! Leveling up '{check_against}'!")
        vocabulary.level_up(random_vocab)
    elif answer == "q" or answer == "quit":
        print("Okay, quitting the game. See you next time!")
        vocabulary.saving()
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
            vocabulary.level_up(random_vocab)
        else:
            print(f"{check_against} will be moved back to level 1.")
            vocabulary.level_down(random_vocab)


vocabulary = flashcards.Vocabulary()

menu()
