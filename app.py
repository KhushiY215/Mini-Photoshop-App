# app.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
from streamlit_drawable_canvas import st_canvas
from utils import apply_filters, crop_image, draw_lines_on_image, add_text_to_image

st.set_page_config(page_title="Mini Photoshop App", layout="wide")
st.title("🖌️ Streamlit Photoshop App")

# Sidebar Controls
with st.sidebar:
    st.header("Image Controls")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    action = st.radio("Choose Action", ["None", "Filters", "Crop", "Draw", "Add Text"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    original_img = img_rgb.copy()

    # FILTERS
    if action == "Filters":
        st.subheader("Adjust Filters")
        blur = st.slider("Blur", 1, 101, 1, step=2)
        brightness = st.slider("Brightness", -100, 100, 0)
        contrast = st.slider("Contrast", 0.5, 3.0, 1.0)
        threshold = st.slider("Threshold", 0, 255, 127)
        img_rgb = apply_filters(original_img, blur, brightness, contrast, threshold)

    # CROP (Preset + Manual)
    elif action == "Crop":
        st.subheader("📐 Preset Crops")
        h, w = img_rgb.shape[:2]
        center_x, center_y = w // 2, h // 2
        col1, col2, col3 = st.columns(3)

        if col1.button("1:1"):
            side = min(h, w)
            x1, y1 = center_x - side // 2, center_y - side // 2
            img_rgb = crop_image(img_rgb, x1, y1, side, side)

        if col2.button("4:3"):
            target_w = min(w, int(h * 4 / 3))
            target_h = int(target_w * 3 / 4)
            x1 = center_x - target_w // 2
            y1 = center_y - target_h // 2
            img_rgb = crop_image(img_rgb, x1, y1, target_w, target_h)

        if col3.button("16:9"):
            target_w = min(w, int(h * 16 / 9))
            target_h = int(target_w * 9 / 16)
            x1 = center_x - target_w // 2
            y1 = center_y - target_h // 2
            img_rgb = crop_image(img_rgb, x1, y1, target_w, target_h)

        st.markdown("---")
        st.subheader("✏️ Manual Crop (Draw rectangle)")

        canvas_crop = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=2,
            stroke_color="#ff0000",
            background_image=Image.fromarray(img_rgb).convert("RGBA"),
            update_streamlit=True,
            height=img_rgb.shape[0],
            width=img_rgb.shape[1],
            drawing_mode="rect",
            key="manual_crop"
        )

        if canvas_crop.json_data and canvas_crop.json_data["objects"]:
            obj = canvas_crop.json_data["objects"][0]
            left = int(obj["left"])
            top = int(obj["top"])
            width = int(obj["width"])
            height = int(obj["height"])
            st.write(f"Selected → x: {left}, y: {top}, w: {width}, h: {height}")
            if st.button("✂️ Apply Manual Crop"):
                img_rgb = crop_image(img_rgb, left, top, width, height)

    # DRAW
    elif action == "Draw":
        st.subheader("Freehand Drawing")
        stroke_color = st.color_picker("Stroke color", "#ff0000")
        stroke_width = st.slider("Stroke width", 1, 25, 5)

        canvas_draw = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_image=Image.fromarray(img_rgb).convert("RGBA"),
            update_streamlit=True,
            height=img_rgb.shape[0],
            width=img_rgb.shape[1],
            drawing_mode="freedraw",
            key="drawing"
        )

        if canvas_draw.json_data and canvas_draw.json_data["objects"]:
            img_rgb = draw_lines_on_image(img_rgb, canvas_draw.json_data["objects"])

    # ADD TEXT
    elif action == "Add Text":
        st.subheader("📝 Add Text to Image")
        text = st.text_input("Enter your text", "Hello, world!")
        font_size = st.slider("Font Size", 10, 100, 30)
        color = st.color_picker("Text Color", "#ff0000")

        st.markdown("➡️ Draw a rectangle on image to position text (adjustable)")
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",  # fully transparent
            stroke_width=1,
            stroke_color=color,
            background_image=Image.fromarray(img_rgb).convert("RGBA"),
            update_streamlit=True,
            height=img_rgb.shape[0],
            width=img_rgb.shape[1],
            drawing_mode="rect",
            key="add_text_area"
        )

        if canvas_result.json_data and canvas_result.json_data["objects"]:
            rect_obj = canvas_result.json_data["objects"][0]
            x = int(rect_obj["left"])
            y = int(rect_obj["top"])
            w = int(rect_obj["width"])
            h = int(rect_obj["height"])
            st.write(f"Text will appear at: (x={x}, y={y})")

            if st.button("➕ Add Text"):
                img_rgb = add_text_to_image(img_rgb, text, x, y, font_size, color)




    # Show result
    st.image(img_rgb, caption="Edited Image", use_column_width=True)

    # Download Button
    result_img = Image.fromarray(img_rgb)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    result_img.save(temp_file.name)
    st.download_button("📥 Download Result", data=open(temp_file.name, "rb"), file_name="edited_image.png", mime="image/png")

else:
    st.info("Please upload an image to get started.")
