# 🖌️ Mini Photoshop App

A web-based photo editor built using **Streamlit** and **OpenCV**, offering basic Photoshop-like features — all accessible from your browser! Upload an image and start editing instantly with filters, cropping, drawing, and text overlay.

---

## ✨ Features

- 🎨 **Image Filters**  
  Adjust Gaussian Blur, Brightness, Contrast, and apply Thresholding.

- ✂️ **Cropping Tools**  
  - Preset aspect ratios: `1:1`, `4:3`, `16:9`  
  - Manual cropping: Draw a custom rectangle directly on the image

- 🖊️ **Freehand Drawing**  
  Pick stroke color and width to sketch directly on the image.

- 🔤 **Add Text**  
  Type and place custom text on the image with your choice of font size and color.

- 📍 **Live Pixel Color** (optional enhancement)  
  Display RGB value of any hovered pixel.

- 📥 **Download Edited Image**  
  Easily download your final output as PNG.

---

## 📁 File Structure

```
mini-photoshop-app/
├── app.py # Main Streamlit app
├── utils.py # Image processing utilities
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

---

## 🚀 Getting Started

### 🔧 1. Install Requirements

```bash
pip install -r requirements.txt
```
✅ Recommended Python version: 3.8 to 3.10

## ▶️ 2. Run the App
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

## 📦 Requirements
- streamlit
- opencv-python-headless
- Pillow
- numpy
- streamlit-drawable-canvas

All included in requirements.txt


## 🧠 Future Improvements
- Image resizing and rotation tools

- Layer support

- Undo/redo functionality

- Save session history

🤝 Contributing
Pull requests are welcome! If you’d like to suggest new features or report a bug, please open an issue.

📜 License
This project is open-source and available under the MIT License.

Built by Khushi❤🤟
