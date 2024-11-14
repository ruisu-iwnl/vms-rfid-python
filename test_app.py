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

        # Step 1: Convert to grayscale (simplified)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Step 2: Apply adaptive histogram equalization to improve contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)

        # Step 3: Apply a simple binary threshold to enhance contrast further
        _, thresh = cv2.threshold(enhanced_gray, 127, 255, cv2.THRESH_BINARY)

        # Show the thresholded image to visualize the filter effect
        thresh_image_b64 = encode_image_to_base64(thresh)

        # Step 4: Use EasyOCR to read text from the enhanced image
        result = reader.readtext(thresh)

        if not result:
            return "No text detected", thresh_image_b64, ""

        # Step 5: Filter results by confidence score (greater than 0.5)
        detected_texts = [item[-2].upper() for item in result if item[-1] > 0.5]
        detected_text = ' '.join(detected_texts)

        # Step 6: Filter for valid plate characters (numbers and uppercase letters)
        detected_text = ''.join(filter(str.isalnum, detected_text))

        # Step 7: Render the result with bounding box and detected text
        font = cv2.FONT_HERSHEY_SIMPLEX
        for (bbox, text, prob) in result:
            if prob > 0.5:  # Confidence threshold
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                cv2.rectangle(open_cv_image, top_left, bottom_right, (0, 255, 0), 3)
                cv2.putText(open_cv_image, text, (top_left[0], top_left[1] - 10), font, 1, (0, 255, 0), 2)

        # Return the final detected text and thresholded image
        return detected_text, thresh_image_b64, ""

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
    detected_text, thresh_image_b64, _ = process_frame(frame_data)  # Process the image to extract text
    emit('update_text', {'text': detected_text, 'thresh_image': thresh_image_b64})  # Send detected text and images back to frontend

# Route for the test page
@app.route('/test')
def test_route():
    return render_template('test.html')

if __name__ == '__main__':
    # Start the Flask app with SSL context
    context = (cert_path, key_path)
    socketio.run(app, debug=True, host='0.0.0.0', port=8443, ssl_context=context)
