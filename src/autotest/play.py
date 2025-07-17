import json
import time
import string
import pyautogui
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController

keyboard = KeyboardController()

# Mapeo para teclas especiales
from pynput.keyboard import Key

key_map = {
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "alt_gr": getattr(Key, "alt_gr", Key.alt),
    "enter": Key.enter,
    "space": Key.space,
    "tab": Key.tab,
    "backspace": Key.backspace,
    "esc": Key.esc,
    "delete": Key.delete,
    "insert": Key.insert,
    "home": Key.home,
    "end": Key.end,
    "page_up": Key.page_up,
    "page_down": Key.page_down,
    "left": Key.left,
    "right": Key.right,
    "up": Key.up,
    "down": Key.down,
    "caps_lock": Key.caps_lock,
    "cmd": Key.cmd,
    "menu": Key.menu,
    "num_lock": Key.num_lock,
    "scroll_lock": Key.scroll_lock,
    "pause": Key.pause,
    "print_screen": Key.print_screen
}


def parse_key(k):
    k_lower = k.lower()
    if k_lower in key_map:
        return key_map[k_lower]
    elif len(k) == 1 and k in string.printable:
        return k
    else:
        print(f"⚠️ Unknown key during playback: {k}")
        return None  # Opcional: podrías lanzar excepción o ignorar


def run(input_file):
    with open(input_file) as f:
        events = json.load(f)

    if not events:
        print("No events to replay.")
        return

    start = time.time()
    base_time = events[0]['time']

    for e in events:
        # Esperar hasta que corresponda el evento
        delay = e['time'] - base_time
        time.sleep(max(0, delay - (time.time() - start)))

        if e['type'] == 'click' and e['pressed']:
            pyautogui.click(x=e['x'], y=e['y'])

        elif e['type'] == 'key_press':
            k = parse_key(e['key'])
            if k is None:
                continue  # o error para abortar

        elif e['type'] == 'key_release':
            k = parse_key(e['key'])
            if k is None:
                continue  # o error para abortar
            keyboard.release(k)
            
