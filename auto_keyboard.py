# PyAutoGUI is a cross-platform GUI automation Python module for human beings.
# Used to programmatically control the mouse & keyboard.
# https://pypi.org/project/PyAutoGUI/
import pyautogui

# This module provides various time-related functions.
# https://docs.python.org/3/library/time.html
import time

#with open(r'autokeys.txt') as write_this:
#    contents = write_this.read()

contents = "\t"
count = 1
enter = "\n"
while True:
    type_this = contents + enter
    time.sleep(15)
    pyautogui.typewrite(type_this, interval=0.001)
    print(count)
    print()
    contents += contents
    count += 1
