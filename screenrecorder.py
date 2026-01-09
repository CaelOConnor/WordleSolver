# uses opencv and mss to screenshot the screen for wordle and then play the game.
# using mss instead of pyautogui because it supports multiple monitors.

import cv2
import mss
import numpy as np

def get_size():
    with mss.mss() as sct:
        print(sct.monitors[2])

def take_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot_width = 500
        screenshot_height = 750

        # The screen part to capture
        # monitor = {
        #     "top": monitor["top"] + monitor["height"] // 2 - screenshot_height // 2,
        #     "left": monitor["left"] + monitor["width"] // 2 - screenshot_width // 2,
        #     "width": screenshot_width,
        #     "height": screenshot_height
        # }
        monitor = {
            "top": monitor["top"] + monitor["height"] // 2 - screenshot_height // 2 + 10,
            "left": monitor["left"] + monitor["width"] // 2 - screenshot_width // 2,
            "width": screenshot_width,
            "height": screenshot_height - 10
        }
        output = "center.png"

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
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
    

def whole_row_is_green():
    pass
    
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
        else:
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

    img = take_screenshot()
    board = crop_board(img)
    boardc = trim_board(board)
    keyboard = crop_keyboard(img)

    #tile = get_tile(boardc, 0, 0)

    for row in range(6):
        for c in range(5):
            tile = get_tile(boardc, row, c)
            #cv2.imshow(f"tile {0},{c}", tile)
            print(tile_is_empty(tile))
            cv2.waitKey(50)

    
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