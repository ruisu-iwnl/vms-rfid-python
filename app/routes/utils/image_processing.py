import base64
import numpy as np
import cv2
import easyocr
from io import BytesIO
from PIL import Image
import imutils

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def process_frame(frame_data):
    try:
        # Decode the base64 image data from the frontend
        img_data = base64.b64decode(frame_data.split(',')[1])
        image = Image.open(BytesIO(img_data))
        
        # Convert image to OpenCV format (BGR)
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Step 1: Grayscale the image
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Step 2: Noise reduction with bilateral filter
        bfilter = cv2.bilateralFilter(gray, 9, 75, 75)
        edged = cv2.Canny(bfilter, 10, 100)

        # Step 3: Find contours and apply mask
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break

        # If no contour found, return message
        if location is None:
            return "No plate detected"

        # Create a mask for the plate region
        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [location], 0, 255, -1)
        cropped_image = cv2.bitwise_and(open_cv_image, open_cv_image, mask=mask)

        # Step 4: Use EasyOCR to read text from the image
        result = reader.readtext(cropped_image)
        
        if not result:
            return "No text detected"

        # Extract all detected text regions and join them
        detected_texts = [item[-2].upper() for item in result if item[-1] > 0.5]  # Confidence > 0.5
        text = ' '.join(detected_texts)
        print("Detected Text:", text)

        return text

    except Exception as e:
        return f"Error processing image: {str(e)}"
