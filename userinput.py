# this file is for having the user input what letters where gray, green and yellow

import os
import numpy as np
import pandas as pd
from collections import Counter
import random

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

    # guess bassed on on info from prev info
    def next_guess(self, guess_letters):
        possible_words = self.words.copy()
        possible_words = possible_words[~possible_words.isin(self.guessed_words)]
        greens = set()
        yellows = set()

        for ltr in guess_letters:
            let = ltr.let.lower()
            if ltr.color == "green":
                greens.add(let)
            elif ltr.color == "yellow":
                yellows.add(let)

        for ltr in guess_letters:
            let, col, pos = ltr.let.lower(), ltr.color, ltr.pos

            if col == "gray": # sub cases ofr gray because of duplicate letter edge cases
                if let not in greens and let not in yellows: # remove all words with the gray letter
                    possible_words = possible_words[~possible_words.str.contains(let)] # words = word[not words that contains that letter]
                elif let in greens and let not in yellows: # words all words except ones that have the green letter
                    green_positions = [ltr.pos for ltr in guess_letters if ltr.let.lower() == let and ltr.color == "green"]
                    mask = pd.Series(False, index=possible_words.index)
                    for pos_idx in green_positions:
                        mask |= possible_words.str[pos_idx] == let
                    possible_words = possible_words[mask]
                elif let not in greens and let in yellows: # remove all words that have that letter in the gray spot and yellow but not the others
                    mask = possible_words.str[pos] != let
                    yellow_positions = [ltr.pos for ltr in guess_letters if ltr.let.lower() == let and ltr.color == "yellow"]
                    yellow_mask = pd.Series(False, index=possible_words.index)
                    for yp in yellow_positions:
                        yellow_mask |= possible_words.str[yp] != let
                    possible_words = possible_words[mask & yellow_mask] # combine masks

            elif col == "green":
                possible_words = possible_words[possible_words.str[pos] == let] # contains the letters
            elif col == "yellow":
                mask = possible_words.str.contains(let) # contains the ltters but not in that spot
                mask &= possible_words.str[pos] != let
                possible_words = possible_words[mask]
            
        if possible_words.empty:
            print("No possible words left.")
            return None

        guess = random.choice(possible_words.tolist())
        print("Next guess:", guess)
        self.guessed_words.add(guess)
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
    