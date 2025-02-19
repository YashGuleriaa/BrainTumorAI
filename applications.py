import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
import joblib

# Load trained model
model = joblib.load("Brain_Tumor_Model.joblib")

def preprocess_image(image_path):
    """Preprocess image for model prediction."""
    img = cv2.imread(image_path, 0)  # Read in grayscale
    img = cv2.resize(img, (200, 200))  # Resize
    img = img.reshape(1, -1) / 255.0  # Flatten and normalize
    return img

def predict_tumor():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = preprocess_image(file_path)
        prediction = model.predict(img)[0]  # Get prediction
        result_text.set("Tumor Detected" if prediction == 1 else "No Tumor")
        
        # Display image
        img_display = Image.open(file_path)
        img_display = img_display.resize((250, 250))
        img_display = ImageTk.PhotoImage(img_display)
        image_label.config(image=img_display)
        image_label.image = img_display  # Keep a reference

# Create main window
root = tk.Tk()
root.title("Brain Tumor Detection")
root.geometry("400x550")

# Heading
heading_label = tk.Label(root, text="Check for Brain Tumor", font=("Arial", 16, "bold"))
heading_label.pack(pady=10)

# Image Upload Button
upload_button = tk.Button(root, text="Upload Image", command=predict_tumor, font=("Arial", 12))
upload_button.pack(pady=10)

# Label to Show Image
image_label = tk.Label(root)
image_label.pack()

# Result Display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 14, "bold"), fg="red")
result_label.pack(pady=10)

# Run application
root.mainloop()
