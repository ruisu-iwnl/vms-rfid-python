import os
import cv2
import easyocr
import imutils
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
from io import BytesIO
from PIL import Image
import numpy as np

# Flask app and SocketIO setup
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'app', 'templates'))
socketio = SocketIO(app)

# EasyOCR Reader initialization
reader = easyocr.Reader(['en'])

# Paths for the SSL certificates
linux_cert_path = '/etc/ssl/certs/selfsigned-cert.pem'
linux_key_path = '/etc/ssl/private/selfsigned-key.pem'
windows_cert_path = r'C:\certs\selfsigned-cert.pem'
windows_key_path = r'C:\certs\selfsigned-key.pem'

# Choose certificate paths based on OS
if os.name == 'nt':
    cert_path = windows_cert_path
    key_path = windows_key_path
else:
    cert_path = linux_cert_path
    key_path = linux_key_path

# Global variables for plate detection
detected_plate = None
detected_text_history = []  # Track last few detections to handle repetitions
plate_detection_threshold = 5  # How many times the same plate should be detected before stopping
plate_detected_flag = False  # Flag to stop processing once plate is detected

# Function to process frames with EasyOCR and OpenCV
def process_frame(frame_data):
    global detected_plate, detected_text_history, plate_detected_flag
    if plate_detected_flag:  # If the plate has been detected, skip further processing
        return f"Plate already detected: {detected_plate}"

    try:
        # Decode the base64 image data from the frontend
        img_data = base64.b64decode(frame_data.split(',')[1])
        image = Image.open(BytesIO(img_data))
        
        # Convert image to OpenCV format (BGR)
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Step 1: Grayscale the image
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Step 2: Noise reduction with lower bilateral filter parameters
        bfilter = cv2.bilateralFilter(gray, 9, 75, 75)  # Reduced parameters for clarity
        edged = cv2.Canny(bfilter, 10, 100)  # Lowered Canny thresholds

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
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        cropped_image = cv2.bitwise_and(open_cv_image, open_cv_image, mask=mask)

        # Step 4: Use EasyOCR to read text from multiple regions, with filtering
        result = reader.readtext(cropped_image)
        
        if not result:
            return "No plate detected"

        # Extract all detected text regions with confidence filtering and join them
        detected_texts = [item[-2].upper() for item in result if item[-1] > 0.5]  # Confidence > 0.5
        text = ' '.join(detected_texts)
        print("Detected Text:", text)

        # Check if the detected text is consistent over time
        detected_text_history.append(text)
        
        # Keep the list length within the threshold
        if len(detected_text_history) > plate_detection_threshold:
            detected_text_history.pop(0)  # Remove the oldest detection

        # If the same plate is detected consecutively (based on history), stop further scanning
        if detected_text_history.count(text) >= plate_detection_threshold:
            detected_plate = text
            plate_detected_flag = True  # Set the flag to stop further processing
            return f"Plate detected: {detected_plate}"

        return f"Detecting plate... Current text: {text}"

    except Exception as e:
        return f"Error processing image: {str(e)}"

# SocketIO event to process frames sent from frontend
@socketio.on('frame')
def handle_frame(data):
    frame_data = data['image']  # Image is sent from frontend as base64
    detected_text = process_frame(frame_data)  # Process the image to extract text
    emit('update_text', {'text': detected_text})  # Send detected text back to frontend

# Route for the test page
@app.route('/test')
def test_route():
    return render_template('test.html')

if __name__ == '__main__':
    # Start the Flask app with SSL context
    context = (cert_path, key_path)
    socketio.run(app, debug=True, host='0.0.0.0', port=8443, ssl_context=context)
