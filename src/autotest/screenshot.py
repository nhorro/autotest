import mss
import mss.tools
import subprocess
from pathlib import Path
from .window import get_window_geometry

def capture_monitor(path, monitor=1):
    """Captura pantalla completa del monitor N."""
    with mss.mss() as sct:
        if monitor >= len(sct.monitors):
            raise ValueError(f"Monitor {monitor} not available. Found {len(sct.monitors)-1} monitors.")
        region = sct.monitors[monitor]
        img = sct.grab(region)
        mss.tools.to_png(img.rgb, img.size, output=str(Path(path)))

def capture_window(path, window_title):
    """Captura solo la región de la ventana cuyo título coincide."""
    region = get_window_geometry(window_title)
    with mss.mss() as sct:
        img = sct.grab(region)
        mss.tools.to_png(img.rgb, img.size, output=str(Path(path)))
