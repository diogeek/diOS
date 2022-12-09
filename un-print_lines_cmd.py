import os
from pynput.keyboard import Key, Listener

CURSOR_UP = "\033[1A"
CURSOR_DOWN = "\033[1B"
NEXT_LINE = "\033[1E"
SET_THIRD_ROW ="\033[3;0H"
CLEAR = "\x1b[2K"
CLEAR_RIGHT = "\x1b[0K"
CLEAR_DOWN = "\x1b[0J"
os.system('')
def hide_cursor():
    print('\033[?25l', end="")
def show_cursor():
    print('\033[?25h', end="")

hide_cursor()

dictspecialchar={Key.enter:"\n",Key.space:" ",Key.tab:"\t"}

def checkchar(key,text):
    try:
        if key==Key.backspace:
            if not text=="":
                return(text[:-1])
            else:
                return("")
        elif key in dictspecialchar.keys():
            return text+dictspecialchar[key]
        else :
            try: return text+(str(key.char))
            except: return text
    except Exception as e:
        print(e)
        input()
text=""
def on_press(key):
    global text
    try:
        text=checkchar(key,text)
        print(f"{SET_THIRD_ROW}{CLEAR_DOWN}{text}|",)
    except Exception as e:
        print(e)

def on_release(key):
    global text
    print(repr(text))
    if key == Key.esc:
        return False

print("A\nA\n")
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
"""
text=""
while 1:
    print(f"{CURSOR_UP}{CLEAR}{text}|",)
"""
