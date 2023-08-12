import numpy as np
import cv2
from PIL import Image
import os

def remove_green_screen(input_path, output_path):
    # Load the image
    img = cv2.imread(input_path)

    # Convert the image from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color of green screen in BGR
    green_screen_color_bgr = np.uint8([[[0, 255, 0]]]) 

    # Convert the green screen color to HSV
    green_screen_hsv = cv2.cvtColor(green_screen_color_bgr, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green_hsv = np.array([green_screen_hsv[0][0][0] - 25, 42, 42])
    upper_green_hsv = np.array([green_screen_hsv[0][0][0] + 25, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green_hsv, upper_green_hsv)

    # Morphological operations
    mask = cv2.dilate(mask, None, iterations=0)
    mask = cv2.erode(mask, None, iterations=0)

    # Create an alpha channel with the same shape as the green screen mask
    alpha_channel = np.ones(mask.shape, dtype=np.uint8) * 255

    # Make the green screen area transparent
    alpha_channel[mask > 0] = 0

    # Add the alpha channel to the image
    img = cv2.merge((img, alpha_channel))

    # Convert the image from OpenCV's default BGR format to RGB, and save it with transparency
    Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)).save(output_path)

# Directory containing the input images
input_dir = 'input/'

# Directory to save the output images
output_dir = 'output/'

# List of all image files in the input directory
image_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]

# Total number of images
total_images = len(image_files)

# Iterate over all the images in the input directory
for i, filename in enumerate(image_files):
    # Full path to the input image
    input_path = os.path.join(input_dir, filename)
    # Full path to save the output image
    output_path = os.path.join(output_dir, filename)
    # Remove the green screen
    remove_green_screen(input_path, output_path)
    # Print progress
    print(f'Processing file {i+1} of {total_images}: {filename}')
