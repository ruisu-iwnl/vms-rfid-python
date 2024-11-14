import base64
import numpy as np
import cv2
import easyocr
from io import BytesIO
from PIL import Image
import imutils

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to process frames with EasyOCR and OpenCV
def process_frame(frame_data):
    try:
        # Decode the base64 image data
        img_data = base64.b64decode(frame_data.split(',')[1])
        image = Image.open(BytesIO(img_data))

        # Convert image to OpenCV format
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Increase resolution (resize image)
        height, width = open_cv_image.shape[:2]
        open_cv_image = cv2.resize(open_cv_image, (width * 2, height * 2))

        # Preprocess image (grayscale, blur, threshold)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

        # Encode processed image to base64 for frontend display
        closed_image_b64 = encode_image_to_base64(closed)

        # Use EasyOCR to detect text
        result = reader.readtext(closed)

        if not result:
            return "No text detected", "", closed_image_b64

        # Sanitize detected text (remove non-alphanumeric characters)
        detected_text = ''.join(filter(str.isalnum, ' '.join([item[-2].upper() for item in result if item[-1] > 0.5])))

        # Print bounding box size (width, height) for each detected text
        for (bbox, text, prob) in result:
            if prob > 0.5: 
                top_left, top_right, bottom_right, bottom_left = map(lambda x: tuple(map(int, x)), bbox)

                letter_width = bottom_right[0] - top_left[0]
                letter_height = bottom_right[1] - top_left[1]

                print(f"Detected letter: '{text}' | Width: {letter_width} pixels, Height: {letter_height} pixels")

                cv2.rectangle(open_cv_image, top_left, bottom_right, (0, 255, 0), 3)
                cv2.putText(open_cv_image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return detected_text, "", closed_image_b64

    except Exception as e:
        return f"Error processing image: {str(e)}", "", ""

# Encode OpenCV image to base64
def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')
