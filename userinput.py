# this file is for having the user input what letters where gray, green and yellow

import os
import numpy as np
import pandas as pd
from collections import Counter
import random

vowels = ['a', 'e', 'u', 'i', 'o', 'y']

class letter:

    def __init__(self, let, color, pos):
        self.let = let
        self.color = color
        self.pso = pos


class solver:

    def __init__(self, words_file='words.txt'):
        self.words = pd.read_csv(words_file, header=None)[0]
        self.words = self.words.str.lower()

    # first word
    def first_word(self):
        vowel_heavy_words = words.map(lambda c: sum([Counter(c.lower()).get(i, 0) for i in vowels ]) >= 3)
        word_to_guess = random.choice(vowel_heavy_words)
        print("For your first word you should guess: ", word_to_guess)

    # get info from user
    def get_info(self):
        letter1 = input("Please enter the first letter:")
        color1 = input("Please enter the first letters color (gray, yellow, or green): ")
        letter2 = input("Please enter the second letter:")
        color2 = input("Please enter the second letters color (gray, yellow, or green): ")
        letter3 = input("Please enter the third letter:")
        color3 = input("Please enter the third letters color (gray, yellow, or green): ")
        letter4 = input("Please enter the fourth letter:")
        color4 = input("Please enter the fourth letters color (gray, yellow, or green): ")
        letter5 = input("Please enter the fifth letter:")
        color5 = input("Please enter the fifth letters color (gray, yellow, or green): ")

    # guess bassed on on info from prev info
    def next_guess(self, let1, col1, let2, col2, let3, col3, let4, col4, let5, col5):
        letters = [let1.lower(), let2.lower(), let3.lower(), let4.lower(), let5.lower()]
        colors = [col1.lower(), col2.lower(), col3.lower(), col4.lower(), col5.lower()]

        possible_words = words.copy()

        for i in range(5):
            if colors[i] == 'gray':
                possible_words = possible_words[
                    ~possible_words.str.contains(letters[i])
                ]

            if colors[i] == 'green':
                if i == 0:
                    possible_words = possible_words[possible_words.str[0] == letters[i]]
                if i == 1:
                    possible_words = possible_words[possible_words.str[1] == letters[i]]
                if i == 2:
                    possible_words = possible_words[possible_words.str[2] == letters[i]]
                if i == 3:
                    possible_words = possible_words[possible_words.str[3] == letters[i]]
                if i == 4:
                    possible_words = possible_words[possible_words.str[4] == letters[i]]

            else: # yellow
                if colors[i] == 'yellow':
                    possible_words = possible_words[
                        possible_words.str.contains(letters[i])
                    ]
                    if i == 0:
                        possible_words = possible_words[possible_words.str[0] != letters[i]]
                    if i == 1:
                        possible_words = possible_words[possible_words.str[1] != letters[i]]
                    if i == 2:
                        possible_words = possible_words[possible_words.str[2] != letters[i]]
                    if i == 3:
                        possible_words = possible_words[possible_words.str[3] != letters[i]]
                    if i == 4:
                        possible_words = possible_words[possible_words.str[4] != letters[i]]

        if len(possible_words) == 0:
            print("No possible words left.")
            return None

        guess = random.choice(possible_words.tolist())
        print("Next guess:", guess)
        return guess




if __name__ == "__main__":
    main()
    