import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QFileDialog, QLineEdit, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import torch
from model import HTSModel

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def preprocess_image(image_path):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Error: Could not read image {image_path}")
            return None
        
        # Crop the bottom 70 pixels (1280x890)
        cropped_img = img[:-70, :]  # 1280x890
        
        # Calculate the starting points for the 890x890 crop from the center
        start_x = (cropped_img.shape[1] - 890) // 2
        start_y = 0  # Starting vertically from the top
        
        # Crop the middle 890x890 region
        middle_cropped_img = cropped_img[start_y:start_y + 890, start_x:start_x + 890]
        
        # Min-max scaling to normalize the image to range 0-1
        min_val = np.min(middle_cropped_img)
        max_val = np.max(middle_cropped_img)
        scaled_img = (middle_cropped_img - min_val) / (max_val - min_val)
        
        # Resize to 256x256 for processing (this won't be shown, just stored in 'image')
        resized_img = cv2.resize(scaled_img, (256, 256))
        
        return middle_cropped_img, resized_img  # 890x890 to show, 256x256 for processing
    
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {e}")
        return None, None


class K10X(QWidget):
    def __init__(self):
        super().__init__()

        # Create an instance of the HTSModel
        self.model = HTSModel()

        # Load the model weights (state dict)
        self.model.load_state_dict(torch.load(resource_path("10kx_weights.pth")))

        # Set the model to evaluation mode
        self.model.eval()
        
        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Import button
        self.import_button = QPushButton("Import Image", self)
        self.import_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.import_button)

        # Input field for text
        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Layer thickness [µm]")
        self.input_text.setVisible(False)
        self.layout.addWidget(self.input_text)
        
        # Predict button
        self.predict_button = QPushButton("Predict", self)
        self.predict_button.setVisible(False)
        self.predict_button.clicked.connect(self.predict)  # Connect to the prediction function
        self.layout.addWidget(self.predict_button)

        # Result label to display the prediction
        self.result_label = QLabel("", self)
        self.result_label.setStyleSheet("color: white;")  # Set text color to white
        self.layout.addWidget(self.result_label)

        # Image display area
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        
        self.original_pixmap = None  # Store the original image as a QPixmap
        
        # Set up initial UI state
        self.setLayout(self.layout)

    def open_file_dialog(self):
        # File selection dialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", 
                                                   "Images (*.png *.xpm *.jpg *.jpeg *.tif)")
        if file_name:
            self.load_and_process_image(file_name)
            self.input_text.setVisible(True)
            self.predict_button.setVisible(True)

    def load_and_process_image(self, image_path):
        # Preprocess the image
        cropped_image, self.processed_image = preprocess_image(image_path)
        
        if cropped_image is not None:
            # Convert NumPy array to QImage
            height, width = cropped_image.shape
            bytes_per_line = width  # since it's grayscale, 1 byte per pixel
            
            # Convert NumPy array to bytes
            image_bytes = cropped_image.tobytes()

            # Create QImage from bytes
            qimage = QImage(image_bytes, width, height, bytes_per_line, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)
            
            # Store the original pixmap
            self.original_pixmap = pixmap

            # Scale the image proportionally to the window size
            self.resize_image()

    def resize_image(self):
        if self.original_pixmap:
            # Get the current size of the window, with padding for layout (-50 for padding)
            available_width = min(self.width() - 50, 890)  # Cap at 890 for width
            available_height = min(self.height() - 50, 890)  # Cap at 890 for height

            # Scale the pixmap proportionally within the size limits
            scaled_pixmap = self.original_pixmap.scaled(
                available_width, available_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Set the scaled pixmap to the label
            self.image_label.setPixmap(scaled_pixmap)

    def predict(self):
        # Get thickness value from input field
        try:
            thickness_value = float(self.input_text.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid float value for thickness.")
            return
        
        if self.processed_image is None:
            QMessageBox.warning(self, "No Image", "Please import an image first.")
            return
        
        # Convert the processed image (256x256) to a PyTorch tensor
        image_tensor = torch.tensor(self.processed_image, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

        # Convert the thickness to a tensor
        thickness_tensor = torch.tensor([[thickness_value]], dtype=torch.float32)

        # Perform inference
        with torch.no_grad():
            predicted_current = self.model(image_tensor, thickness_tensor)

        # Display the predicted critical current
        self.result_label.setText(f"Predicted Critical Current: {int(predicted_current.item())} A")

    
    def resizeEvent(self, event):
        # Resize the image proportionally when the window is resized
        self.resize_image()
        super().resizeEvent(event)