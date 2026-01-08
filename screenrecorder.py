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
        monitor = {
            "top": monitor["top"] + monitor["height"] // 2 - screenshot_height // 2,
            "left": monitor["left"] + monitor["width"] // 2 - screenshot_width // 2,
            "width": screenshot_width,
            "height": screenshot_height
        }
        output = "center.png"

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        #print(output)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) #BGR
        return img

#def get_tile_from_screenshot():
    

#def check_left_most_tiles(img):


def crop_board(img): # img is a numpy array
    h, w, channels = img.shape 
    top = 0
    bottom = int(h * 0.55)
    left = 0
    right = w
    return img[top:bottom, left:right]

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
    # fix keyboard crop
    board = crop_board(img)
    keyboard = crop_keyboard(img)

    #cv2.imshow("uncropped board", img)
    cv2.imshow("board", board)
    cv2.imshow("keyboard", keyboard)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()