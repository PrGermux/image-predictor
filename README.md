# Neural Network Image Predictor

This Python project is a neural network-based tool that evaluates images based on user-provided textual input. The application utilizes PyQt5 for the graphical user interface and PyTorch for neural network implementation. It allows users to upload grayscale images and provide corresponding text input (e.g., a numerical value), with the application processing both inputs to predict an output value.

### Key Features:
- **Multi-Tab Interface**: The application provides a tabbed interface, allowing users to switch between different prediction models or views.
- **Image Preprocessing**: The tool automatically crops and resizes images, ensuring consistent input for the neural network. Images are cropped to remove unwanted portions and are scaled to 256x256 resolution for optimal model performance.
- **Text and Image Input**: Users can input images and related numerical text (e.g., thickness) into the tool. The neural network uses both inputs to generate a prediction, making it ideal for tasks where visual and numerical data must be processed together.
- **Neural Network Architecture**: The neural network has a carefully designed structure with multiple convolutional layers for image feature extraction, followed by fully connected layers that combine the image features with the numerical input. This allows for a more refined prediction based on both inputs.

### Why This Structure?
- **Image Resolution**: The images are resized to 256x256 pixels because this is a common input size for convolutional neural networks, balancing computational efficiency and maintaining enough detail from the images.
- **Network Complexity**: The network is composed of multiple convolutional layers followed by pooling, which helps extract features from the image in a hierarchical manner. The fully connected layers combine these features with the numerical input, allowing the model to learn complex patterns from both visual and text data. This structure ensures that the model can handle the dual input sources efficiently, making accurate predictions.
- **Neurons Allocation**: The network uses a large number of neurons in the fully connected layers (128, 64) to ensure that the rich feature set extracted from the images and text data can be adequately processed. This helps the network capture more nuanced relationships between the inputs and the output.

### Usage
This tool is useful for scenarios where both visual and text data need to be analyzed together. It could be applicable in various fields such as medical imaging, industrial inspections, or scientific research where predictions are based on both image characteristics and external measurements.

### Python Branch and Complexity
- **Python Branch**: This project showcases the combination of PyQt5 for creating an interactive graphical interface and PyTorch for building and deploying a neural network. It demonstrates proficiency in both graphical UI design and machine learning model integration.
- **Complexity**: The project is moderately complex, involving both GUI development and deep learning. The architecture is designed for tasks where image and numerical inputs are both necessary to generate accurate predictions. The neural network architecture is highly efficient, leveraging convolutional layers for feature extraction and fully connected layers for final predictions.

### Code Structure
- **Main Interface**: The interface uses QTabWidget to organize different views and models, allowing easy switching between different tasks or configurations.
- **Image Preprocessing**: The images are cropped and scaled to ensure consistent input size for the neural network, enhancing model performance.
- **Model**: The neural network model is implemented using PyTorch, with separate layers for processing images and numerical inputs, followed by layers that combine these inputs to generate predictions.

### Future Enhancements
- **Additional Model Tabs**: Support more tabs for different neural network models or different prediction tasks.
- **Real-Time Prediction**: Add real-time prediction capabilities where users can stream or continuously input new images for instant feedback.
- **Data Augmentation**: Implement data augmentation techniques such as image rotations, flips, and brightness adjustments to improve the model's robustness.
- **Magnified Images**: For fine structures train magnified images.

## Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/c88eeced-ee27-4539-9217-cd8d57e76338"/>
</p>

## Usage
**WARNING:** This program works only with images and text inputs formatted specifically for the neural network. Users must follow the image processing and input instructions carefully.

Run the main application:
```sh
python main.py
```

## Freezing
To create an executable file, use the following command:
```sh
pyinstaller --onedir --windowed --icon=icon.png --add-data "icon.png;." --add-data "10kx_weights.pth;." --hidden-import=scipy.special._cdflib --name "Image Predictor" main.py
```

## Dependencies
- Python 3.x
- PyQt5
- PyTorch
- OpenCV
- NumPy

## License
This project is licensed under the MIT License for non-commercial use.
