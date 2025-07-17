# autotest

**autotest** es una herramienta liviana para grabar y reproducir secuencias de teclado y mouse sobre aplicaciones gráficas en Linux. Está pensada para automatizar pruebas funcionales sobre UIs, generar scripts visuales y validar flujos reproducibles. También permite capturar ventanas y trabajar de forma integrada con Jupyter Notebooks.

---

## ✨ Características

- Grabación y reproducción fiel de eventos reales (teclado, mouse, combinaciones)
- Captura de pantallas por ventana o monitor
- Espera condicional de ventanas antes de ejecutar
- Uso desde terminal, scripts o notebooks
- Salida editable en formato `.json`

---

## 📦 Instalación

### 🔧 Requisitos del sistema (Ubuntu)

```bash
sudo apt update
sudo apt install xdotool x11-utils gedit
````

### 🐍 Requisitos Python

Instalación editable:

```bash
pip install -e .
```

Esto instalará `autotest` como comando de consola y sus dependencias (`pynput`, `pyautogui`, `mss`).

---

## 🚀 Ejemplos de uso

### Grabar y reproducir una secuencia

```bash
autotest record -o test.json
autotest play -i test.json
```

### Capturar una ventana

```bash
autotest screenshot -o captura.png -w "gedit"
```

### Listar ventanas activas

```bash
autotest list-windows
```

---

## 🧪 Ejemplo completo (gedit)

```bash
gedit &  # lanza la app

autotest record -o test_gedit.json
# Durante la grabación: escribí algo, hacé Ctrl+S, nombrá el archivo, Enter

autotest play -i test_gedit.json
autotest screenshot -o resultado.png -w "gedit"
```

---

## 📔 Uso desde Jupyter Notebook

```python
from autotest.notebook_utils import play_from_notebook

play_from_notebook(
    input_file="test_gedit.json",
    window_title="gedit",
    screenshot_path="resultado.png",
    delay_before=3
)
```

---

## 📌 Notas

* Funciona solo en entornos Linux con X11.
* No requiere modificar las aplicaciones bajo prueba.
* Los archivos `.json` generados son legibles y editables.

---