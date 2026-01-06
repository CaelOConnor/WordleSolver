# uses opencv and mss to screenshot the screen for wordle and then play the game.
# using mss instead of pyautogui because it supports multiple monitors.

import cv2
import mss
import numpy as np

def get_size():
    with mss.mss() as sct:
        print(sct.monitors[2])

def take_screenshoot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot_width = 500
        screenshot_height = 1080

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
        print(output)

def main():
    #size = get_size()
    img = take_screenshoot()

if __name__ == "__main__":
    main()