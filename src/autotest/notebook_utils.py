import subprocess
import time
from pathlib import Path
from IPython.display import Image, display
from autotest.screenshot import capture_window
from autotest.window import wait_for_window

def play_from_notebook(input_file, *, window_title=None, screenshot_path=None, delay_before=3):
    """
    Ejecuta un test en segundo plano desde notebook y muestra una captura al final.
    
    Args:
        input_file (str): path al archivo JSON de eventos.
        window_title (str): si se especifica, espera a que la ventana esté presente.
        screenshot_path (str): si se especifica, guarda y muestra captura luego del test.
        delay_before (float): tiempo antes de lanzar el test, para mover el foco si es necesario.
    """
    if window_title:
        print(f"🕐 Esperando ventana: '{window_title}'...")
        wait_for_window(window_title, timeout=10)

    if delay_before:
        print(f"⌛ Esperando {delay_before} segundos para que muevas el foco...")
        time.sleep(delay_before)

    print(f"▶️ Ejecutando: {input_file}")
    subprocess.run(["autotest", "play", "-i", input_file])

    if screenshot_path and window_title:
        print(f"📸 Capturando ventana: {window_title}")
        capture_window(screenshot_path, window_title=window_title)
        display(Image(screenshot_path))
