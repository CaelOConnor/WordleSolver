A Python-based Wordle solver that plays the game directly in the browser using computer vision.
The solver takes a screenshots of the game board, recognizes the letters, colors, and positions. Then the solver determines the next best word and types it into the browser and continues this process until it has the word or the board is full.
Screenshots are captured using mss, allowing the program to work on multi-monitor setups.
Letter recognition is performed using OpenCV template matching.
The solver interacts with the website via pyautogui
word.txt file from darkermango on github link here: https://github.com/darkermango/5-Letter-words/blob/main/docs/words.txt 