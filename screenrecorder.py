# uses opencv and mss to screenshot the screen for wordle and then play the game.
# using mss instead of pyautogui because it supports multiple monitors

import cv2
import mss
import numpy as np
import os
import time
import pyautogui
import userinput

class WebSolver:
    def __init__(self):
        self.templates = self.load_templates()

    # get size of screen
    def get_size(self):
        with mss.mss() as sct:
            print(sct.monitors[2])

    # will have to change for other monitors or single monitor setups
    def take_screenshot(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot_width = 500
            screenshot_height = 750
            monitor = {
                "top": monitor["top"] + monitor["height"] // 2 - screenshot_height // 2 + 10,
                "left": monitor["left"] + monitor["width"] // 2 - screenshot_width // 2,
                "width": screenshot_width,
                "height": screenshot_height - 10
            }
            output = "center.png"
            sct_img = sct.grab(monitor)
            img = np.array(sct_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) #BGR
            return img

    # return pic of wordle square
    def get_tile(self, board, row, col): 
        h, w, channels = board.shape 
        tile_h = h // 6
        tile_w = w // 5
        top = row * tile_h
        bottom = (row + 1) * tile_h
        left = col * tile_w
        right = (col + 1) * tile_w
        return board[top:bottom, left:right]

    def tile_is_empty(self, tile):
        gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
        # Look at the center area where letters appear
        h, w = gray.shape
        center = gray[h//4:3*h//4, w//4:3*w//4]
        return np.std(center) < 10

    def get_tile_color(self, tile):
        h, w, channels = tile.shape
        y = int(h * 0.15) # pixel a letter wont touch
        x = int(w * 0.15)

        b, g, r = tile[y, x] # get vallues at that spot
        if abs(int(b) - int(g)) < 10 and abs(int(b) - int(r)) < 10:
            return "gray"
        if g > r + 25 and g > b + 25:
            return "green"
        return "yellow"

    def whole_row_is_green(self, board, row):
        green_counter = 0
        for col in range(0, 5):
            tile = self.get_tile(board, row, col)
            if self.get_tile_color(tile) == 'green':
                green_counter += 1
        if green_counter == 5:
            return True
        else:
            return False

    # preprocess for cv
    def preprocess_tile_for_letter(self, tile):
        gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY) # Letter becomes white
        # Remove noise
        kernel = np.ones((2, 2), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        return thresh

    # center for cv
    def center_letter(self, binary, size=40):
        ys, xs = np.where(binary > 0)

        if len(xs) == 0:
            return np.zeros((size, size), dtype=np.uint8)

        top, bottom = ys.min(), ys.max()
        left, right = xs.min(), xs.max()
        letter = binary[top:bottom+1, left:right+1]
        h, w = letter.shape
        # Create square canvas so all letters are the same size for template matching
        canvas = np.zeros((max(h, w), max(h, w)), dtype=np.uint8)
        y_off = (canvas.shape[0] - h) // 2 # centering the letter
        x_off = (canvas.shape[1] - w) // 2
        canvas[y_off:y_off+h, x_off:x_off+w] = letter
        return cv2.resize(canvas, (size, size))

    def load_templates(self):
        templates = {}
        for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            img = cv2.imread(f"letter_pics/letters_{ch}.png")
            processed = self.preprocess_tile_for_letter(img)
            centered = self.center_letter(processed)
            templates[ch] = centered
        return templates

    def recognize_letter(self, tile):
        processed = self.preprocess_tile_for_letter(tile)
        centered = self.center_letter(processed)
        best_score = 0
        best_letter = None

        for letter, tmpl in self.templates.items():
            res = cv2.matchTemplate(centered, tmpl, cv2.TM_CCOEFF_NORMED)
            score = res[0][0]

            if score > best_score:
                best_score = score
                best_letter = letter

        if best_score < 0.4:
            return None

        return best_letter

    def trim_board(self, board):
        gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY) # convert to grayscale
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY) # turns image intop a black and white mask _ is return value but we dont need it
        # crop sides
        col_sum = np.sum(thresh, axis=0)
        cols = np.where(col_sum > 0)[0]
        left = cols[0]
        right = cols[-1]
        # crop top and bottom
        row_sum = np.sum(thresh, axis=1)
        rows = np.where(row_sum > 0)[0]
        top = rows[0]
        bottom = rows[-1]
        trimmed = board[top:bottom, left:right]
        #cv2.imwrite("board_trimmed.png", trimmed)
        return trimmed

    def crop_board(self, img): # img is a numpy array
        h, w, channels = img.shape 
        top = 0
        bottom = int(h * 0.55)
        left = 0
        right = w
        board = img[top:bottom, left:right]
        #cv2.imwrite("board.png", board)
        return board

    def crop_keyboard(self, img): # img is a numpy array
        h, w, channels = img.shape
        top = int(h * 0.55)
        bottom = h
        left = 0
        right = w
        return img[top:bottom, left:right]

    def type_guess(self, guess):
        print("Typing guess:", guess)
        time.sleep(3)
        for ch in guess:
            pyautogui.press(ch)
        pyautogui.press("enter")

    def get_info_of_previous(self, board, row):
        letters = []
        for col in range(5):
            tile = self.get_tile(board, row, col)
            color = self.get_tile_color(tile)
            letter = self.recognize_letter(tile)
            info = userinput.Letter(letter, color, col)
            letters.append(info)
        return letters

    def find_current_row(self, board):
        for row in range(6):
            if self.tile_is_empty(self.get_tile(board, row, 0)):
                return row
        return None


def main():
    webSolver = WebSolver()
    #templates = load_templates()
    solver = userinput.Solver()
    while True:
        img = webSolver.take_screenshot()
        board = webSolver.trim_board(webSolver.crop_board(img))
        row = webSolver.find_current_row(board)
        if row is None:
            print("Game over (board full)")
            return
        if row == 0:
            guess = solver.first_word()
        else:
            letters = webSolver.get_info_of_previous(board, row-1)

            if webSolver.whole_row_is_green(board, row-1):
                print("We won!")
                return
            guess = solver.next_guess(letters)
        webSolver.type_guess(guess)
        time.sleep(4)  # wait for animation

if __name__ == "__main__":
    main()