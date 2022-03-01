import random
import termcolor

level_1 = {}  # every day
level_2 = {}  # every 3 days
level_3 = {}  # every week
level_4 = {}  # every 2 weeks
level_5 = {}  # every month
level_6 = {}  # long-term memory, never, #final


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
                    cont = input(
                        "Done! Term saved to vocabulary! Keep going? y/n: ")
    menu()


def practising_vocabulary():
    # creating dict out of all levels
    global testing_vocabulary
    testing_vocabulary = {k: v
                          for d in (
                              level_1, level_2, level_3, level_4, level_5, level_6)
                          for k, v in d.items()}

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


menu()


# TO DO
# differentiate between entire vocabulary & vocabulary that needs testing (2 different dicts)
# --> I can only do this once there's time stamps on the vocabs


# level_1 = {"term": "translation",
#            "Guten Morgen": "Goedemorgen", "ihr": "jullie"}
