# utils.py
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def apply_filters(image, blur, brightness, contrast, threshold):
    k = blur if blur % 2 == 1 else blur + 1
    image = cv2.GaussianBlur(image, (k, k), sigmaX=0)
    image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(thresh_img, cv2.COLOR_GRAY2RGB)

def crop_image(img, x, y, w, h):
    return img[y:y+h, x:x+w]

def draw_lines_on_image(img, objects):
    img_pil = Image.fromarray(img).convert("RGBA")
    draw = ImageDraw.Draw(img_pil)

    for obj in objects:
        if obj["type"] == "path":
            path = obj["path"]
            points = []
            for item in path:
                if len(item) >= 3:
                    x, y = item[1], item[2]
                    points.append((x, y))
            if len(points) >= 2:
                draw.line(points, fill=obj["stroke"], width=int(obj["strokeWidth"]))
    return np.array(img_pil)

def add_text_to_image(img, text, x, y, size, hex_color):
    img_pil = Image.fromarray(img).convert("RGBA")
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype("arial.ttf", size)
    except:
        font = ImageFont.load_default()
    draw.text((x, y), text, font=font, fill=hex_color)
    return np.array(img_pil)


