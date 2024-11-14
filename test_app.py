import os
import cv2
import easyocr
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

# SSL certificate paths (adjust to your platform)
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

# Function to process frames with EasyOCR and OpenCV
def process_frame(frame_data):
    try:
        # Decode the base64 image data from the frontend
        img_data = base64.b64decode(frame_data.split(',')[1])
        image = Image.open(BytesIO(img_data))

        # Convert image to OpenCV format (BGR)
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Increase the image resolution by resizing
        height, width = open_cv_image.shape[:2]
        open_cv_image = cv2.resize(open_cv_image, (width * 2, height * 2))  # Resize to 2x the original size

        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Step 2: Apply Gaussian Blur to reduce noise and smooth the image
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Step 3: Apply adaptive thresholding for binarization (black and white image)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

        # Step 4: Apply morphological operations to clean up noise (opening and closing)
        kernel = np.ones((3, 3), np.uint8)
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

        # Show the thresholded and morphologically processed image to visualize the effect
        closed_image_b64 = encode_image_to_base64(closed)

        # Step 5: Use EasyOCR to read text from the processed image
        result = reader.readtext(closed)

        if not result:
            return "No text detected", "", closed_image_b64

        # Step 6: Filter results by confidence score (greater than 0.5)
        detected_texts = [item[-2].upper() for item in result if item[-1] > 0.5]
        detected_text = ' '.join(detected_texts)

        # Step 7: Filter for valid plate characters (numbers and uppercase letters)
        detected_text = ''.join(filter(str.isalnum, detected_text))

        # Step 8: Render the result with bounding box and detected text
        font = cv2.FONT_HERSHEY_SIMPLEX
        for (bbox, text, prob) in result:
            if prob > 0.5:  # Confidence threshold
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                cv2.rectangle(open_cv_image, top_left, bottom_right, (0, 255, 0), 3)
                cv2.putText(open_cv_image, text, (top_left[0], top_left[1] - 10), font, 1, (0, 255, 0), 2)

        # Return the final detected text and processed image
        return detected_text, "", closed_image_b64

    except Exception as e:
        return f"Error processing image: {str(e)}", "", ""

def encode_image_to_base64(image):
    """Encode an OpenCV image to base64."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

# SocketIO event to process frames sent from frontend
@socketio.on('frame')
def handle_frame(data):
    frame_data = data['image']  # Image is sent from frontend as base64
    detected_text, _, closed_image_b64 = process_frame(frame_data)  # Process the image to extract text
    emit('update_text', {'text': detected_text, 'processed_image': closed_image_b64})  # Send detected text and processed image back to frontend

# Route for the test page
@app.route('/test')
def test_route():
    return render_template('test.html')

if __name__ == '__main__':
    # Start the Flask app with SSL context
    context = (cert_path, key_path)
    socketio.run(app, debug=True, host='0.0.0.0', port=8443, ssl_context=context)
