# this file is for having the user input what letters where gray, green and yellow

import os
import numpy as np
import pandas as pd
from collections import Counter
import random
import sys

vowels = ['a', 'e', 'u', 'i', 'o', 'y']

class Letter:

    def __init__(self, let, color, pos):
        self.let = let.upper()
        self.color = color.lower()
        self.pos = pos 
    
    def __repr__(self):
        return f"Letter(let='{self.let}', color='{self.color}', pos={self.pos})"

class Solver:

    def __init__(self, words_file='words.txt'):
        self.words = pd.read_csv(words_file, header=None)[0]
        self.words = self.words.str.lower()
        self.guessed_words = set()

        self.known_greens = {}
        self.known_yellows = {} 
        self.known_gray = set()
        self.letter_min = Counter() 
        self.letter_max = {}   

    # first word
    def first_word(self):
        vowel_heavy_words = []

        for word in self.words:
            vowel_count = 0

            for v in vowels:
                vowel_count += word.count(v)

            if vowel_count >= 3:
                vowel_heavy_words.append(word)

        if not vowel_heavy_words:
            print("No vowel-heavy words found.")
            return None

        word_to_guess = random.choice(vowel_heavy_words)
        print("For your first word you should guess:", word_to_guess)
        self.guessed_words.add(word_to_guess)
        return word_to_guess

    # get info from user
    def get_info(self):
        guess = []
        print("Please input the guess and its information: ")
        for pos in range(5):
            let = input(f"Letter {pos + 1}: ").strip().lower()
            color = input("Color (green or yellow or gray): ").strip().lower()
            while color not in {"green", "yellow", "gray"}:
                color = input("Invalid color. Enter green, yellow, or gray: ").strip().lower()
            guess.append(Letter(let, color, pos))
        return guess
    
    def update_knowledge(self, guess_letters):
        per_guess_min = Counter()     # green and yellow counts 
        per_guess_total = Counter()   # total occurrences 

        for ltr in guess_letters:
            let = ltr.let.lower()
            per_guess_total[let] += 1

            if ltr.color in ("green", "yellow"):
                per_guess_min[let] += 1

            if ltr.color == "green":
                self.known_greens[ltr.pos] = let

            elif ltr.color == "yellow":
                self.known_yellows.setdefault(let, set()).add(ltr.pos)

        for let, count in per_guess_min.items():
            self.letter_min[let] = max(self.letter_min.get(let, 0), count)

        # gray
        for let, total in per_guess_total.items():
            if let not in per_guess_min:
                # fully gray letter
                self.known_gray.add(let)
            elif total > per_guess_min[let]:
                # gray + green/yellow => exact count known
                self.letter_max[let] = self.letter_min[let]

    # guess bassed on on info from prev info
    def next_guess(self, guess_letters):
        # Update global knowledge
        self.update_knowledge(guess_letters)

        possible_words = self.words.copy()
        possible_words = possible_words[~possible_words.isin(self.guessed_words)]

        # greens 
        for pos, let in self.known_greens.items():
            possible_words = possible_words[possible_words.str[pos] == let]

        # yellows
        for let, bad_positions in self.known_yellows.items():
            mask = possible_words.str.contains(let)
            for pos in bad_positions:
                mask &= possible_words.str[pos] != let
            possible_words = possible_words[mask]

        # gray
        for let in self.known_gray:
            possible_words = possible_words[~possible_words.str.contains(let)]

        # min counts
        for let, min_c in self.letter_min.items():
            possible_words = possible_words[possible_words.str.count(let) >= min_c]

        # max counts
        for let, max_c in self.letter_max.items():
            possible_words = possible_words[possible_words.str.count(let) <= max_c]

        if possible_words.empty:
            print("No possible words left.")
            sys.exit(0)

        guess = random.choice(possible_words.tolist())
        self.guessed_words.add(guess)
        print("Next guess:", guess)
        return guess


def main():
    solver = Solver()
    firstword = solver.first_word()
    guess_counter = 1
    while guess_counter <= 5:
        user_guess = solver.get_info()
        #print(user_guess)
        finished = input("Did you guess the word correctly? (y/n): ").strip().lower()
        if finished == "y":
            print(f"Congratulations! You solved it in {guess_counter} guesses.")
            break
        next_guess_to_use = solver.next_guess(user_guess)
        guess_counter += 1

if __name__ == "__main__":
    main()
    