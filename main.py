import csv
import random
from contextlib import suppress

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import wikipedia
from colorama import Fore
from colorama import init
from random_word import RandomWords  # https://pypi.org/project/Random-Word/ generates a random word


def intro():
    """
    Sound advice for making effective initial guesses
    :return: None
    """
    print('''
    \nHerbert S. Zim, in his classic introductory cryptography text "Codes and Secret Writing", gives the English letter
frequency sequence as "ETAON RISHD LFCMU GYPWB VKJXZQ", the most common letter pairs as "TH HE AN RE ER IN ON AT ND ST 
ES EN OF TE ED OR TI HI AS TO", and the most common doubled letters as "LL EE SS OO TT FF RR NN PP CC". 

The "top twelve" letters constitute about 80% of the total usage. The "top eight" letters constitute about 65% of the 
total usage.''')
    question = input('\nTry a test word: y/N ')
    if question == 'y':
        test_word = input('Type a test word: ')
        hangman(list(test_word))
    else:
        hangman()


def hangman(test_word=None):
    """
    instantiates base variables

    :return:
    """
    init(autoreset=True)  # Saves having to keep typing 'Fore.RESET' to have colorama return text colour to the default.
    rw = RandomWords()  # create an instance of a RandomWords object
    if not test_word:
        word = list(rw.get_random_word(hasDictionaryDef="true", minLength=5, maxLength=10, minDictionaryCount=10,
                                       minCorpusCount=50))
    else:
        word = test_word
    word_copy = word.copy()  # compare answer with as the word list above will be changing
    answer = list('_' * len(word))  # answer template
    noose = 0  # incrementer for wrong guesses
    print("\nLet's play Hangman!")
    print('-' * 19, '\n')
    player_go(word, word_copy, answer, noose)


def player_go(*args):
    """
    instantiates each turn and processes guess whether it's in or not in word

    :param args: word, word_copy, answer, noose
    :return:
    """
    word, word_copy, answer, noose = args
    guessed_letters = []
    total_guesses = 11
    while answer != word_copy:
        guess = input('\nGuess a letter: ')
        guessed_letters.append(guess)  # list for processing
        glj = ', '.join(guessed_letters)  # string for appearance

        if guess not in word:
            total_guesses -= 1
            guesses_left = Fore.LIGHTRED_EX + str(total_guesses) + Fore.RESET
            print('\n' * 50)  # clears the screen for the next go
            print(
                f'\n"{guess.upper()}" is not in the word.\n\nGuessed Letters: {glj.upper()}.\n\nYou are {guesses_left} '
                f'wrong answers from the noose! Have another go...')
            print('\nword:', Fore.LIGHTWHITE_EX + ''.join(answer).upper(), '\n')
            noose += 1  # trigger for advancing build of the gallows
            gallows(noose, word_copy, guessed_letters)  # initiates gallows function

        else:
            # while loop to check if guessed letter appears in word as index method will only find first one. pop
            # removes the first instance so if there any more of them they can be found. This means if a guessed
            # letter appears more than once in the word it will show up as many times as that in the answer meaning
            # you don't have to guess the same letter more than once! Thank you Otis for the feedback!
            while guess in word:
                guesses_left = Fore.LIGHTRED_EX + str(total_guesses) + Fore.RESET
                guess_index = word.index(guess)  # finds index of letter guessed in word
                answer.pop(guess_index)  # removes the element at the index
                answer.insert(guess_index, guess)  # adds the correct guessed letter to the correct index
                word.pop(guess_index)  # repeat of the above
                word.insert(guess_index, '-')  # as above

            display = ''.join(answer)  # looks better formatted as a string
            print('\n' * 50)
            print('word:', Fore.LIGHTWHITE_EX + display.upper())
            print(
                f'\nWell done! "{guess.upper()}" is in the word.\n\nGuessed Letters: {glj.upper()}\n\nYou are {guesses_left} '
                f' wrong answers from the noose! Have another go...')

    print(Fore.GREEN + '\nWell done! You got it!', Fore.LIGHTWHITE_EX + ''.join(answer).upper(),
          Fore.GREEN + 'was the word.\n')
    wikipedia_request(answer, guessed_letters, noose)


def gallows(*args):
    """
    builds the gallows and switches to end game when word guessed / dead

    :param args: noose, word_copy, gl
    :return:
    """
    noose, word_copy, gl = args
    # the function builds the gallows incrementally for each wrong answer
    if noose == 1:
        print(Fore.LIGHTCYAN_EX + ' ========')
    elif noose == 2:
        print(Fore.LIGHTCYAN_EX + '     |/')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + ' =========')
    elif noose == 3:
        print(Fore.LIGHTCYAN_EX + '   =========')
        print(Fore.LIGHTCYAN_EX + '     |/')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + ' =========')
    elif noose == 4:
        print(Fore.LIGHTCYAN_EX + '   =========')
        print(Fore.LIGHTCYAN_EX + '     |/   |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + ' =========')
    elif noose == 5:
        print(Fore.LIGHTCYAN_EX + '   =========')
        print(Fore.LIGHTCYAN_EX + '     |/   |')
        print(Fore.LIGHTCYAN_EX + '     |    O')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + ' =========')
    elif noose == 6:
        print(Fore.LIGHTCYAN_EX + '   =========')
        print(Fore.LIGHTCYAN_EX + '     |/   |')
        print(Fore.LIGHTCYAN_EX + '     |    O')
        print(Fore.LIGHTCYAN_EX + '     |    |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + ' =========')
    elif noose == 7:
        print(Fore.LIGHTCYAN_EX + '   =========')
        print(Fore.LIGHTCYAN_EX + '     |/   |')
        print(Fore.LIGHTCYAN_EX + '     |    O')
        print(Fore.LIGHTCYAN_EX + '     |   \|')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + '     |')
        print(Fore.LIGHTCYAN_EX + ' =========')
    elif noose == 8:
        print(Fore.LIGHTCYAN_EX + '    =========')
        print(Fore.LIGHTCYAN_EX + '      |/   |')
        print(Fore.LIGHTCYAN_EX + '      |    O')
        print(Fore.LIGHTCYAN_EX + '      |   \|/')
        print(Fore.LIGHTCYAN_EX + '      |')
        print(Fore.LIGHTCYAN_EX + '      |')
        print(Fore.LIGHTCYAN_EX + '      |')
        print(Fore.LIGHTCYAN_EX + '  =========')
    elif noose == 9:
        print(Fore.LIGHTCYAN_EX + '    =========')
        print(Fore.LIGHTCYAN_EX + '      |/   |')
        print(Fore.LIGHTCYAN_EX + '      |    O')
        print(Fore.LIGHTCYAN_EX + '      |   \|/')
        print(Fore.LIGHTCYAN_EX + '      |    |')
        print(Fore.LIGHTCYAN_EX + '      |')
        print(Fore.LIGHTCYAN_EX + '      |')
        print(Fore.LIGHTCYAN_EX + '  =========')
    elif noose == 10:
        print(Fore.LIGHTCYAN_EX + '    =========')
        print(Fore.LIGHTCYAN_EX + '      |/   |')
        print(Fore.LIGHTCYAN_EX + '      |    O')
        print(Fore.LIGHTCYAN_EX + '      |   \|/')
        print(Fore.LIGHTCYAN_EX + '      |    |')
        print(Fore.LIGHTCYAN_EX + '      |   / ')
        print(Fore.LIGHTCYAN_EX + '      |')
        print(Fore.LIGHTCYAN_EX + '  ==========')
    elif noose == 11:
        print(Fore.LIGHTRED_EX + '   =========')
        print(Fore.LIGHTRED_EX + '      |/   |')
        print(Fore.LIGHTRED_EX + '      |    O')
        print(Fore.LIGHTRED_EX + '      |   \|/')
        print(Fore.LIGHTRED_EX + '      |    |')
        print(Fore.LIGHTRED_EX + '      |   / \ ')
        print(Fore.LIGHTRED_EX + '      |')
        print(Fore.LIGHTRED_EX + '  =========')
        x = ''.join(word_copy)
        print(Fore.RED + '\nYOU\'RE DEAD!!!', Fore.LIGHTWHITE_EX + x.upper(), Fore.RED + 'was the word.\n')
        wikipedia_request(x, gl, noose)


def wikipedia_request(*args):
    """
    looks up wikipedia information for the word

    :param args: answer, gl, noose
    :return:
    """
    answer, gl, noose = args
    answer = ''.join(answer)
    try:
        print(Fore.LIGHTYELLOW_EX + 'Wikipedia Summary:')
        print(wikipedia.summary(answer))
    except wikipedia.exceptions.DisambiguationError as e:
        print(Fore.LIGHTYELLOW_EX + '\nTop ranking result from Wikipedia disambiguate list:')
        print(wikipedia.summary(e.options[0]))
        print(Fore.LIGHTYELLOW_EX + '\nRandom result from Wikipedia disambiguate list:')
        print(wikipedia.summary(e.options[random.choice(range(len(e.options)))]))
    except wikipedia.exceptions.PageError:
        print(Fore.LIGHTYELLOW_EX + '\nWikipedia search suggestion for', Fore.LIGHTYELLOW_EX + answer + ':')
        print(wikipedia.summary(wikipedia.suggest(answer)))
    finally:
        print(Fore.LIGHTYELLOW_EX + '\nDefinitions:')
        twinword_request(answer, gl, noose)


def twinword_request(*args):
    """
    looks up definitions of word

    :param args: display, gl, noose
    :return:
    """
    display, gl, noose = args
    url = "https://twinword-word-graph-dictionary.p.rapidapi.com/definition/"
    querystring = {"entry": display}
    headers = {
        'x-rapidapi-key': "01ae2be8d8msh2216d12e4f182d1p10e2cejsn1bcfc5c879cd",
        'x-rapidapi-host': "twinword-word-graph-dictionary.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    definition = response.json()
    try:
        print(definition['meaning']['noun'])
        print(definition['meaning']['verb'])
        print(definition['meaning']['adverb'])
        print(definition['meaning']['adjective'])
        check_word_frequency(display, gl, noose)
    except KeyError:
        datamuse_request(display, gl, noose)


def datamuse_request(*args):
    """
    backup if twinword request fails. finally command to move on should this request also fail

    :param args: display, gl, noose
    :return: display, gl, noose
    """
    response = requests.get(f"http://api.datamuse.com//words?sp={args[0]}&md=d")
    x = (response.json())
    try:
        for i in x[0]['defs']:
            print(i)
            check_word_frequency(args[0], args[1], args[2])
    except (IndexError, KeyError):
        pass  # print('None found!')
    finally:
        check_word_frequency(args[0], args[1], args[2])


def check_word_frequency(*args):
    """
    checks if the word is in a list of the top 5000 most frequently used English words. Shows a message if it is

    :param args: word, gl, noose
    :return: word, gl, noose
    """
    with open('word_freq_count.csv', 'r') as file1:  # Top 5,000 entries
        reader1 = csv.reader(file1)
        for row in reader1:
            if args[0].lower() in row:
                if int(row[1]) < 5052:
                    print()
                    print(Fore.LIGHTWHITE_EX + args[0].upper(), 'is', Fore.LIGHTWHITE_EX + row[1], 'of the top '
                                                                                                   '5000 most used '
                                                                                                   'English '
                                                                                                   'words!')
    file1.close()
    scores(args[0], args[1], args[2])


def scores(*args):
    """
    Using scrabble letter points and a sample of 40,000 English words:
    > word score
    > frequency of each unique letter appearing in the word
    > used letter score

    noose is simply being passed between functions to get to the end. Must be a better way!

    :param args: word, guessed_letters, noose
    :return: word, letter_score, scrabble_score, guessed_letters, used_letter_score, noose
    """

    #  dict values are scrabble scores and English Letter Frequency (based on a sample of 40,000 words) respectively.
    letter_score = {
        'E': [1, 12.02],
        'T': [1, 9.10],
        'A': [1, 8.12],
        'O': [1, 7.68],
        'I': [1, 7.31],
        'N': [1, 6.95],
        'S': [1, 6.28],
        'R': [1, 6.02],
        'H': [4, 5.92],
        'D': [2, 4.32],
        'L': [1, 3.98],
        'U': [1, 2.88],
        'C': [3, 2.71],
        'M': [3, 2.61],
        'F': [4, 2.30],
        'Y': [4, 2.11],
        'W': [4, 2.09],
        'G': [2, 2.03],
        'P': [3, 1.82],
        'B': [3, 1.49],
        'V': [4, 1.11],
        'K': [5, 0.69],
        'X': [8, 0.17],
        'Q': [10, 0.11],
        'J': [8, 0.10],
        'Z': [10, 0.7],
    }
    scrabble_score = 0
    letter_frequency_score = 0
    used_letter_score = 0

    # to handle ui if not isalpha
    for letter in args[0].upper():
        with suppress(KeyError):
            scrabble_score += letter_score[letter][0]
            letter_frequency_score += letter_score[letter][1]
    for letter in args[1]:
        with suppress(KeyError):
            used_letter_score += letter_score[letter.upper()][0]

    if args[2] > 10:
        print(Fore.LIGHTWHITE_EX + '\nFinal Score:', Fore.LIGHTRED_EX + 'You died!')
    else:
        final_score = used_letter_score - scrabble_score - len(args[0])
        print(Fore.LIGHTWHITE_EX + '\nFinal Score:', Fore.LIGHTGREEN_EX + str(final_score))
        print('Less is better! A negative number is great!')

    choice = input('\nWant to see some tables? y/N: ')
    if choice == 'y':
        tables(args[0], letter_score, scrabble_score, args[1], used_letter_score)
    else:
        hangman()


def tables(*args):
    """
    Creates 3 matplotlib tables depicting:
    > frequency of each unique letter appearing in the word within a sample of 40,000 English words
    > number of times each letter in the word appears in the word. Scrabble word value in the table header
    > letters guessed, the scrabble point value for each, and sum points of all letters guessed

    :param args: word, letter_score, scrabble_score, guessed_letters, used_letter_score

    """

    scrabble_letter_score = [args[1][letter.upper()][0] for letter in args[0]]  # letter values of every letter in word
    word_list = list(args[0])
    letter_count_list = [word_list.count(letter) for letter in word_list]  # frequency of each unique letter in word
    product = np.multiply(scrabble_letter_score, letter_count_list)  # totals value for every letter (value * frequency)
    d1 = {word_list[i]: int(product[i]) for i in range(len(word_list))}  # (k) letter v(total value) duplicates excluded

    # table 1. letter count
    plt.figure(figsize=(70, 10))
    plt.subplot(1, 4, 1)
    letter_count = [(args[0].count(letter)) for letter in set(args[0])]  # using set counts but hides duplicates!
    dictionary = dict(zip(set(args[0]), letter_count))
    rect = plt.bar([k for k, v in dictionary.items()], [v for k, v in dictionary.items()])
    plt.xlabel(f'Letter')
    plt.ylabel("Letter Count")
    plt.title(f'Word Value ({args[0]}) = {args[2]}')
    plt.yticks([v for k, v in dictionary.items()])

    #  table 2. score per letter
    plt.subplot(1, 4, 2)
    data = {'Letter': d1.keys(),
            'Count': d1.values()}
    df = pd.DataFrame(data, columns=['Letter', 'Count'])
    plots = sns.barplot(x="Letter", y="Count", data=df, palette="Blues_d")
    plots.set(yticklabels=[])
    plots.tick_params(left=False)

    # Iterating over the bars one-by-one
    for bar in plots.patches:
        # Using Matplotlib's annotate function and
        # passing the coordinates where the annotation shall be done
        # x-coordinate: bar.get_x() + bar.get_width() / 2
        # y-coordinate: bar.get_height()
        # free space to be left to make graph pleasing: (0, 8)
        # ha and va stand for the horizontal and vertical alignment
        plots.annotate(format(bar.get_height(), '.2f'),
                       (bar.get_x() + bar.get_width() / 2,
                        bar.get_height()), ha='center', va='center',
                       xytext=(0, 8),
                       textcoords='offset points')

    plt.xlabel("Letter")
    plots.set(ylabel=None)
    plt.title(f"Total points per letter")

    # table 3. frequency table
    plt.subplot(1, 4, 3)
    plt.bar([x for x in args[0]], [args[1][letter][1] for letter in args[0].upper()], color="red")
    plt.xlabel(f'Letter')
    plt.title('Letter Frequency')  # English Letter Frequency (based on a sample of 40,000 words
    plt.yticks([args[1][letter.upper()][1] for letter in args[0]])

    # table 4. guess count table
    glstring = ''.join(args[3])
    plt.subplot(1, 4, 4)
    plt.bar([x for x in glstring], [args[1][letter][0] for letter in glstring.upper()], color="green")
    plt.xlabel(f'Letter')
    plt.ylabel("Scrabble Point")
    plt.title(f'Guess Value = {args[4]}')
    plt.yticks([args[1][letter.upper()][0] for letter in glstring])

    plt.show()
    hangman()


intro()
