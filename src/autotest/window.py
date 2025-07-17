import subprocess
import time

from .screenshot import get_window_geometry

def list_open_window_titles():
    """
    Devuelve una lista de títulos de ventanas visibles (X11, requiere xdotool).
    """
    try:
        # Obtiene IDs de ventanas visibles
        output = subprocess.check_output(["xdotool", "search", "--onlyvisible", "--name", "."], text=True)
        window_ids = output.strip().splitlines()
    except subprocess.CalledProcessError:
        return []

    titles = []
    for win_id in window_ids:
        try:
            title = subprocess.check_output(["xdotool", "getwindowname", win_id], text=True).strip()
            titles.append(title)
        except subprocess.CalledProcessError:
            continue  # puede fallar si una ventana desapareció

    return titles

def wait_for_window(title_substring, timeout=10, poll_interval=0.2):
    """
    Espera hasta que aparezca una ventana visible cuyo título contenga `title_substring`.
    Devuelve la geometría {left, top, width, height}.
    Lanza TimeoutError si no aparece en `timeout` segundos.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        titles = list_open_window_titles()
        for t in titles:
            if title_substring in t:
                return get_window_geometry(t)
        time.sleep(poll_interval)
    raise TimeoutError(f"Window with title containing '{title_substring}' not found within {timeout} seconds.")

