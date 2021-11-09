# PyAutoGUI is a cross-platform GUI automation Python module for human beings.
# Used to programmatically control the mouse & keyboard.
# https://pypi.org/project/PyAutoGUI/
import pyautogui

# This module provides various time-related functions.
# https://docs.python.org/3/library/time.html
import time

with open(r'curl_encoded.txt') as write_this:
    contents = write_this.read()
time.sleep(3)
pyautogui.typewrite(contents, interval=0.001)
