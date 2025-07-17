import mss
import mss.tools
import subprocess
from pathlib import Path

def capture_monitor(path, monitor=1):
    """Captura pantalla completa del monitor N."""
    with mss.mss() as sct:
        if monitor >= len(sct.monitors):
            raise ValueError(f"Monitor {monitor} not available. Found {len(sct.monitors)-1} monitors.")
        region = sct.monitors[monitor]
        img = sct.grab(region)
        mss.tools.to_png(img.rgb, img.size, output=str(Path(path)))

def get_window_geometry(window_title):
    """Devuelve dict con top, left, width, height"""
    try:
        # obtener ID de ventana
        win_id = subprocess.check_output(
            ["xdotool", "search", "--name", window_title],
            text=True
        ).splitlines()[0]

        # obtener geometría
        output = subprocess.check_output(
            ["xwininfo", "-id", win_id],
            text=True
        )

        geom = {}
        for line in output.splitlines():
            if "Absolute upper-left X" in line:
                geom["left"] = int(line.split()[-1])
            elif "Absolute upper-left Y" in line:
                geom["top"] = int(line.split()[-1])
            elif "Width" in line:
                geom["width"] = int(line.split()[-1])
            elif "Height" in line:
                geom["height"] = int(line.split()[-1])

        if len(geom) != 4:
            raise RuntimeError("Incomplete geometry")

        return geom

    except subprocess.CalledProcessError:
        raise RuntimeError(f"Window not found: {window_title}")

def capture_window(path, window_title):
    """Captura solo la región de la ventana cuyo título coincide."""
    region = get_window_geometry(window_title)
    with mss.mss() as sct:
        img = sct.grab(region)
        mss.tools.to_png(img.rgb, img.size, output=str(Path(path)))
