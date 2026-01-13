# uses opencv and mss to screenshot the screen for wordle and then play the game.
# using mss instead of pyautogui because it supports multiple monitors.

import cv2
import mss
import numpy as np
import os
import time
import pyautogui

def get_size():
    with mss.mss() as sct:
        print(sct.monitors[2])

def take_screenshot():
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
        #mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        #print(output)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) #BGR
        return img

def get_tile(board, row, col): # return pic of wordle square
    h, w, channels = board.shape 
    tile_h = h // 6
    tile_w = w // 5
    top = row * tile_h
    bottom = (row + 1) * tile_h
    left = col * tile_w
    right = (col + 1) * tile_w
    return board[top:bottom, left:right]

def tile_is_empty(tile): # change this to return true or false based on color of tile 
    pixel_to_check = tile[5:15, 5:15]
    avg_color = np.mean(pixel_to_check, axis=(0, 1))
    brightness = np.mean(avg_color)
    return brightness < 20 # tweek this value for empty vs gray tiles

def get_tile_color(tile):
    h, w, channels = tile.shape
    y = int(h * 0.15) # pixel a letter wont touch
    x = int(w * 0.15)

    b, g, r = tile[y, x] # get vallues at that spot
    if abs(int(b) - int(g)) < 10 and abs(int(b) - int(r)) < 10:
        return "gray"
    if g > r + 25 and g > b + 25:
        return "green"
    return "yellow"

def whole_row_is_green(board, row):
    green_counter = 0
    for col in range(0, 5):
        tile = get_tile(board, row, col)
        if get_tile_color(tile) == 'green':
            green_counter += 1
    if green_counter == 5:
        return True
    else:
        return False

def preprocess_tile_for_letter(tile):
    gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY) # Letter becomes white
    # Remove noise
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return thresh

def center_letter(binary, size=40):
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

def load_templates():
    templates = {}
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        img = cv2.imread(f"letter_pics/letters_{ch}.png")
        processed = preprocess_tile_for_letter(img)
        centered = center_letter(processed)
        templates[ch] = centered
    return templates

def recognize_letter(tile, templates):
    processed = preprocess_tile_for_letter(tile)
    centered = center_letter(processed)

    # cv2.imshow("tile_processed", centered)
    # cv2.imshow("template_A", templates["A"])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    best_score = 0
    best_letter = None

    for letter, tmpl in templates.items():
        res = cv2.matchTemplate(centered, tmpl, cv2.TM_CCOEFF_NORMED)
        score = res[0][0]

        if score > best_score:
            best_score = score
            best_letter = letter

    if best_score < 0.4:
        return None

    return best_letter


    
def check_left_most_tiles(board):
    tile = get_tile(board, row, 0) # check row 1 to see if we need to do first guess
    if tile_is_empty(tile):
        first_word
    for row in range(1, 6):
        tile = get_tile(board, row, 0)
        if tile_is_empty(tile):
            get_info_of_previous
            next_guess
        elif whole_row_is_green():
            print("We won")
            break
    if whole_row_is_green == False:
        print("We lost")

def trim_board(board):
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

def crop_board(img): # img is a numpy array
    h, w, channels = img.shape 
    top = 0
    bottom = int(h * 0.55)
    left = 0
    right = w
    board = img[top:bottom, left:right]
    
    #cv2.imwrite("board.png", board)

    return board

def crop_keyboard(img): # img is a numpy array
    h, w, channels = img.shape
    top = int(h * 0.55)
    bottom = h
    left = 0
    right = w
    return img[top:bottom, left:right]

def main():
    #size = get_size()
    templates = load_templates()


    # for ch in "AEIOU":
    #     cv2.imshow(ch, templates[ch])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    img = take_screenshot()
    board = crop_board(img)
    boardc = trim_board(board)
    keyboard = crop_keyboard(img)

    #tile = get_tile(boardc, 0, 0)

    for row in range(6):
        for c in range(5):
            tile = get_tile(boardc, row, c)
            #print("tile shape:", tile.shape)
            #cv2.imshow(f"tile {0},{c}", tile)
            #print(tile_is_empty(tile))
            #print(get_tile_color(tile))
            cv2.waitKey(50)
            letter = recognize_letter(tile, templates)
            print(letter)

    
    # for col in range(5):
    #     tile = get_tile(boardc, 0, col)
    #     cv2.imshow(f"tile {0},{col}", tile)

    #find_cur_row()

    #cv2.imshow("uncropped board", img)
    #cv2.imshow("board", board)

    #cv2.imshow("board cropped", boardc)

    #cv2.imshow("keyboard", keyboard)

    #cv2.imshow("top left tile", tile)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()