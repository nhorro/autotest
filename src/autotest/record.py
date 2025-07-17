from pynput import mouse, keyboard
import json
import time

def run(output_file):
    events = []
    start_time = time.time()
    stop_flag = False

    def timestamp():
        return time.time() - start_time

    def to_str(key):
        if hasattr(key, 'char') and key.char is not None:
            return key.char
        elif hasattr(key, 'name'):
            return key.name
        else:
            s = str(key)
            print(f"⚠️ Unknown key during record: {s}")
            return s


    def on_click(x, y, button, pressed):
        events.append({
            'type': 'click',
            'x': x,
            'y': y,
            'button': str(button),
            'pressed': pressed,
            'time': timestamp()
        })

    def on_press(key):
        nonlocal stop_flag
        key_str = to_str(key)

        if key_str == 'esc':
            stop_flag = True
            return False

        events.append({
            'type': 'key_press',
            'key': key_str,
            'time': timestamp()
        })

    def on_release(key):
        key_str = to_str(key)
        events.append({
            'type': 'key_release',
            'key': key_str,
            'time': timestamp()
        })

    with mouse.Listener(on_click=on_click) as ml, \
         keyboard.Listener(on_press=on_press, on_release=on_release) as kl:

        while not stop_flag:
            time.sleep(0.01)

    with open(output_file, "w") as f:
        json.dump(events, f, indent=2)
    print(f"✔️ Recorded to {output_file}")
