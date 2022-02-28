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
    vocabulary = [level_1, level_2, level_3, level_4, level_5, level_6]
    print("This is your vocabulary: ")
    num = 0
    for item in vocabulary:
        print(f"Level {num+1}")
        for key in item:
            print(key, ":", item[key])
        num += 1
    menu()
    # give ooption to update term if you see mistakes or want to add a second definity


def creating_vocabulary():
    cont = "y"
    while cont == "y":
        vocab = input(
            "Please input your term like this: ''term/phrase : translation/definition': ")
        try:
            key, value = vocab.split(" : ")
        except ValueError:
            print(
                "Sorry, something went wrong. Did you follow the guidelines? Try again!")
        else:
            global level_1
            level_1[key] = value
            cont = input("Done! Term saved to vocabulary! Keep going? y/n: ")
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
    if random_vocab in level_1:
        level_2[random_vocab] = level_1[random_vocab]
        level_1.pop(random_vocab)
    elif random_vocab in level_1.values():
        reverse_back = list(level_1.keys())[list(
            level_1.values()).index(random_vocab)]
        level_2[reverse_back] = level_1[reverse_back]
        level_1.pop(reverse_back)
    elif random_vocab in level_2:
        level_3[random_vocab] = level_2[random_vocab]
        level_2.pop(random_vocab)
    elif random_vocab in level_2.values():
        reverse_back = list(level_2.keys())[list(
            level_2.values()).index(random_vocab)]
        level_3[reverse_back] = level_2[reverse_back]
        level_2.pop(reverse_back)
    elif random_vocab in level_3:
        level_4[random_vocab] = level_3[random_vocab]
        level_3.pop(random_vocab)
    elif random_vocab in level_3.values():
        reverse_back = list(level_3.keys())[list(
            level_3.values()).index(random_vocab)]
        level_4[reverse_back] = level_3[reverse_back]
        level_3.pop(reverse_back)
    elif random_vocab in level_4:
        level_5[random_vocab] = level_4[random_vocab]
        level_4.pop(random_vocab)
    elif random_vocab in level_4.values():
        reverse_back = list(level_4.keys())[list(
            level_4.values()).index(random_vocab)]
        level_5[reverse_back] = level_4[reverse_back]
        level_4.pop(reverse_back)
    elif random_vocab in level_5:
        level_6[random_vocab] = level_5[random_vocab]
        level_5.pop(random_vocab)
    elif random_vocab in level_5.values():
        reverse_back = list(level_5.keys())[list(
            level_5.values()).index(random_vocab)]
        level_6[reverse_back] = level_5[reverse_back]
        level_5.pop(reverse_back)
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
# give option to correct or update term in vocabulary
# add colors/fonts (i.e. red if incorrect, green if correct)
# differentiate between entire vocabulary & vocabulary that needs testing (2 different dicts)
# print error message if term already exists
# turn level_up into match case, try this out --> OR turn into for loop
# give option to return to menu while adding to vocabulary (if you accidently typed y)


# level_1 = {"term": "translation",
#            "Guten Morgen": "Goedemorgen", "ihr": "jullie"}

# testing_vocabulary()

# ranli = list(level_1)
# print(ranli)
# random.shuffle(ranli)
# print(ranli[0])
# print(level_1[ranli[0]])


# if vocab is in level 1 - move to level 2
# if vocab in level 2 - move to level 3
# and so on - long list though
# try out match?


# vocab: print all levels, give option to update
# testing: start test(default)
# for now, no way to save longterm, so do not ask which level but always trigger level_1
# shuffle level
# ask: do you want to be asked the word or the translation (default = "translation")
# if testing == "word" --> access level[key]
# elif testing == "translation" --> access level[value]
# else --> default to access level[value]

# gives you translation, you have to type in word
# if typed in word == level[key] --> move into next level
# elif typed word != level[key] --> show word, ask if correct (y/n)
# if "y" --> move into next level
# if "n" keep in current level
