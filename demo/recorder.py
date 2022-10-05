from pynput.mouse import Listener
import time
import json
import redis

from keeper.environments import SystemEnv

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
session_file = "session_test.json"
with open(session_file, "w") as f:
    f.write("")


def update(item):
    queue_name = "mouse_data"
    r = redis.Redis(host="localhost", port=6379, db=0)
    prev_item = r.lrange(queue_name, -1, -1)
    if prev_item:
        prev_item = json.loads(prev_item[0])
    # Released
    if item['button'] == 'Left' and item['state'] == 'Released':
        r.rpush(queue_name, json.dumps(item))
        # {MM}*DD
        if prev_item and prev_item['state'] != 'Pressed':
            print("DD:", r.lrange(queue_name, 0, -1))
        # {MM}*PC
        if prev_item and prev_item['state'] == 'Pressed':
            print("PC:", r.lrange(queue_name, 0, -1))
        # new action
        r.delete(queue_name)
    # Move
    else:
        if SystemEnv.X_MIN <= int(item['x']) <= SystemEnv.X_MAX \
        and SystemEnv.Y_MIN <= int(item['y']) <= SystemEnv.Y_MAX:
            r.rpush(queue_name, json.dumps(item))


def on_move(x, y):
    item = {
        "client timestamp": time.time(),
        "button": "NoButton",
        "state": "Move",
        "x": x,
        "y": y
    }
    update(item)
    with open(session_file, "a") as f:
        f.write("{}\n".format(json.dumps(item)))


def on_click(x, y, button, pressed):
    item = {
        "client timestamp": time.time(),
        "button": button.name.capitalize(),
        "state": "Pressed" if pressed else "Released",
        "x": x,
        "y": y
    }
    update(item)
    with open(session_file, "a") as f:
        f.write("{}\n".format(json.dumps(item)))


def on_scroll(x, y, dx, dy):
    item = {
        "client timestamp": time.time(),
        "button": "Scroll",
        "state": "Down" if dy < 0 else "Up",
        "x": x,
        "y": y
    }
    with open(session_file, "a") as f:
        f.write("{}\n".format(json.dumps(item)))


# Collect events
with Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll) as listener:
    listener.join()
