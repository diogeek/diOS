import os
CURSOR_UP = "\033[1A"
CLEAR = "\x1b[2K"
os.system('')

while 1:
    print(f"{CURSOR_UP}{CLEAR}{input('>>>')}")
