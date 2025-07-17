import subprocess
import time
import subprocess

def get_window_geometry(window_title, min_width=300, min_height=200):
    """
    Busca ventanas visibles cuyo título contenga `window_title` y devuelve la geometría
    (left, top, width, height) de la más grande que cumpla con tamaño mínimo.
    """
    try:
        win_ids = subprocess.check_output(
            ["xdotool", "search", "--onlyvisible", "--name", window_title],
            text=True
        ).strip().splitlines()
    except subprocess.CalledProcessError:
        raise RuntimeError(f"No windows found with title matching: {window_title}")

    best = None
    for win_id in win_ids:
        try:
            output = subprocess.check_output(["xwininfo", "-id", win_id], text=True)
            geom = {}
            for line in output.splitlines():
                if "Absolute upper-left X" in line:
                    geom["left"] = int(line.split()[-1])
                elif "Absolute upper-left Y" in line:
                    geom["top"] = int(line.split()[-1])
                elif "Width:" in line:
                    geom["width"] = int(line.split()[-1])
                elif "Height:" in line:
                    geom["height"] = int(line.split()[-1])
            if geom["width"] >= min_width and geom["height"] >= min_height:
                best = geom
                break
        except subprocess.CalledProcessError:
            continue

    if not best:
        raise RuntimeError(f"No visible window with title '{window_title}' and minimum size found.")

    return best


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

