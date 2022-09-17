from pynput.mouse import Listener
import time


"""
# Sample data:
{
    "client timestamp": 0,
    "button": "NoButton",
    "state": "Move",
    "x": 492,
    "y": 499
}
"""


def on_move(x, y):
    data = {
        "client timestamp": time.time(),
        "button": "NoButton",
        "state": "Move",
        "x": x,
        "y": y
    }
    print(data)


def on_click(x, y, button, pressed):
    data = {
        "client timestamp": time.time(),
        "button": button.name.capitalize(),
        "state": "Pressed" if pressed else "Released",
        "x": x,
        "y": y
    }
    print(data)


def on_scroll(x, y, dx, dy):
    data = {
        "client timestamp": time.time(),
        "button": "Scroll",
        "state": "Down" if dy < 0 else "Up",
        "x": x,
        "y": y
    }
    print(data)


# Collect events
with Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()
