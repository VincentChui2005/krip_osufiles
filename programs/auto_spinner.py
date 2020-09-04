"""Requires raw input off"""
from pynput.keyboard import Listener, Key
from pynput.mouse import Controller, Button
import cmath


trigger = "d"
distance = 200
click_key = Button.left
quit_key = Key.delete


mouse = Controller()

# Find middle point
nowpos = mouse.position
pos = mouse.position
mouse.move(1, 1)
while pos != mouse.position:
    pos = mouse.position
    mouse.move(1, 1)
mouse.position = nowpos
resolution = pos[0] + 1, pos[1] + 1
middle = resolution[0] / 2, resolution[1] / 2


def get_angle():
    dist, angle = cmath.polar((mouse.position[0] - middle[0]) + (mouse.position[1] - middle[1]) * 1j)
    if angle < 0: angle = 2 * cmath.pi + angle
    return dist, angle


def on_press(key):
    try:
        if key.char == trigger:
            mouse.press(click_key)

            dist, angle = get_angle()
            angle += cmath.pi / 1.1
            pos = cmath.rect(distance, angle)
            mouse.position = pos.real + middle[0], pos.imag + middle[1]
    except AttributeError:
        if key == quit_key: quit()


def on_release(key):
    try:
        if key.char == trigger:
            mouse.release(click_key)
    except AttributeError: pass


with Listener(on_press, on_release) as listener:
    listener.join()

