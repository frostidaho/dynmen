from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import Xlib.XK
from time import sleep
import os


display = Display(os.getenv('DISPLAY'))

getkey = lambda x: display.keysym_to_keycode(Xlib.XK.string_to_keysym(x))

retkey = getkey('Return')
spacekey = getkey('space')

d_keys = {
    ' ': spacekey,
}

def str_to_keycodes(txt):
    for char in txt:
        try:
            yield d_keys[char]
        except KeyError:
            val = getkey(char)
            d_keys[char] = val
            yield val

def type_str(txt):
    display.sync()
    sleep(0.3)
    for key in str_to_keycodes(txt):
        sleep(0.1)
        fake_input(display, X.KeyPress, key)
        fake_input(display, X.KeyRelease, key)
        display.sync()

def hit_enter():
    retkey = getkey('Return')
    sleep(0.1)
    display.sync()
    fake_input(display, X.KeyPress, retkey)
    fake_input(display, X.KeyRelease, retkey)
    display.sync()


