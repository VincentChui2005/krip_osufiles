from pynput.keyboard import Listener, Key
from pynput.mouse import Controller, Button


trigger = "d"
click_key = Button.left
quit_key = Key.delete

mouse = Controller()

def on_press(key):
    try:
        if key.char == trigger:
            mouse.press(click_key)
    except AttributeError:
        if key == quit_key: quit()


def on_release(key):
    try:
        if key.char == trigger:
            mouse.release(click_key)
    except AttributeError: pass


with Listener(on_press, on_release) as li: li.join()

