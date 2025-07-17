import cv2
import json
import os
from pathlib import Path

def annotate_image(image_path, output_json="annotations.json", output_dir="templates"):
    regions = []
    start_point = None
    drawing = False
    image = cv2.imread(image_path)
    clone = image.copy()

    def mouse_callback(event, x, y, flags, param):
        nonlocal start_point, drawing, image
        if event == cv2.EVENT_LBUTTONDOWN:
            start_point = (x, y)
            drawing = True
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            end_point = (x, y)
            x0, y0 = start_point
            w, h = x - x0, y - y0
            name = input(f"Etiqueta para región ({x0}, {y0}, {w}, {h}): ")
            regions.append({"name": name, "x": x0, "y": y0, "width": w, "height": h})
            # Guardar template
            os.makedirs(output_dir, exist_ok=True)
            cropped = clone[y0:y0 + h, x0:x0 + w]
            cv2.imwrite(os.path.join(output_dir, f"{name}.png"), cropped)
            cv2.rectangle(image, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow("image", image)

    cv2.imshow("image", image)
    cv2.setMouseCallback("image", mouse_callback)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    with open(output_json, "w") as f:
        json.dump(regions, f, indent=2)
    print(f"✔️ {len(regions)} regiones guardadas en {output_json}")
