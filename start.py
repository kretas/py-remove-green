import numpy as np
import cv2
from PIL import Image

def remove_green_screen(input_path, output_path):
    # Load the image
    img = cv2.imread(input_path)

    # Convert the image from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color of green screen in BGR
    green_screen_color_bgr = np.uint8([[[0, 208, 28]]])  # BGR representation of your green screen color

    # Convert the green screen color to HSV
    green_screen_hsv = cv2.cvtColor(green_screen_color_bgr, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green_hsv = np.array([green_screen_hsv[0][0][0] - 20, 50, 50])
    upper_green_hsv = np.array([green_screen_hsv[0][0][0] + 20, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green_hsv, upper_green_hsv)

    # Desaturate green pixels
    hsv[mask > 0] = [0, 0, 255]

    # Convert back to BGR for saving
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Create an alpha channel with the same shape as the green screen mask
    alpha_channel = np.ones(mask.shape, dtype=np.uint8) * 255

    # Make the green screen area transparent
    alpha_channel[mask > 0] = 0

    # Add the alpha channel to the image
    img = cv2.merge((bgr, alpha_channel))

    # Save it with transparency
    Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)).save(output_path)


# Testing the function
remove_green_screen('test.png', 'output1.png')
