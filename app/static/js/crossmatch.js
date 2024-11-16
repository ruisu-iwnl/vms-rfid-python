function nextStep() {
    document.getElementById('cameraSection').style.display = 'none';
    document.getElementById('rfidSection').style.display = 'block';
    document.getElementById('nextBtn').style.display = 'none';
}

document.getElementById('nextBtn').addEventListener('click', nextStep);

const videoElement = document.getElementById('liveCamera');
const capturedImage = document.getElementById('capturedImage');
const detectedTextElement = document.getElementById('detectedText');
const captureBtn = document.getElementById('captureBtn');
const toggleCameraBtn = document.getElementById('toggleCameraBtn');
const retryBtn = document.getElementById('retryBtn');
const scanningText = document.getElementById('scanningText');
const socket = io.connect('https://' + window.location.hostname + ':8443');

let cameraStream = null;

function toggleCamera() {
    if (cameraStream) {
        const tracks = cameraStream.getTracks();
        tracks.forEach(track => track.stop());
        cameraStream = null;
        videoElement.srcObject = null;
        toggleCameraBtn.textContent = 'Enable Camera';
        videoElement.style.display = 'none';
        captureBtn.style.display = 'none';
    } else {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                cameraStream = stream;
                videoElement.srcObject = stream;
                toggleCameraBtn.textContent = 'Disable Camera';
                videoElement.style.display = 'block';
                captureBtn.style.display = 'inline'; 
            })
            .catch(error => console.error('Error accessing webcam:', error));
    }
}

function captureAndSendFrame() {
    scanningText.style.display = 'block';
    typeScanningText("Scanning... Please wait.");
    document.getElementById('progressBarContainer').style.display = 'block';
    
    let progress = 0;
    const progressBar = document.getElementById('progressBar');
    
    const progressInterval = setInterval(() => {
        progress += 5;
        if (progress >= 100) {
            clearInterval(progressInterval);
        }
        progressBar.style.width = progress + '%';
    }, 500);

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    const frame = canvas.toDataURL('image/jpeg');

    capturedImage.src = frame;
    capturedImage.style.display = 'none';
    videoElement.style.display = 'none';
    captureBtn.style.display = 'none';
    toggleCameraBtn.style.display = 'none';
    retryBtn.style.display = 'inline';

    document.getElementById('nextBtn').style.display = 'inline-block';

    socket.emit('frame', { image: frame });
}

socket.on('update_text', (data) => {
    detectedTextElement.textContent = "Detected Plate Number: " + data.text;
    detectedTextElement.style.display = 'block';
    scanningText.style.display = 'none';
    document.getElementById('progressBarContainer').style.display = 'none';
});

function retryCapture() {
    location.reload();
}

captureBtn.addEventListener('click', captureAndSendFrame);
retryBtn.addEventListener('click', retryCapture);
toggleCameraBtn.addEventListener('click', toggleCamera);

socket.on('update_text', (data) => {
    detectedTextElement.textContent = "Detected Plate Number: " + data.text;
    detectedTextElement.style.display = 'block';
    scanningText.style.display = 'none';
});

function typeScanningText(text) {
    let i = 0;
    scanningText.textContent = "";
    const typingSpeed = 100;

    function type() {
        if (i < text.length) {
            scanningText.textContent += text.charAt(i);
            i++;
            setTimeout(type, typingSpeed);
        } else {
            setTimeout(() => {
                scanningText.textContent = '';
                i = 0;
                type();
            }, 1000);
        }
    }

    type();
}
