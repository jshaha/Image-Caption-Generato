import cv2  # OpenCV is a library to work with images

# Preprocess the image to get it ready for the model
def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)  # Read the image file
    image = cv2.resize(image, (224, 224))  # Resize to the required size for VGG16 (224x224)
    image = image / 255.0  # Normalize the image so that pixel values are between 0 and 1
    image = image.reshape((1, 224, 224, 3))  # Reshape for the model (batch size 1)
    return image
