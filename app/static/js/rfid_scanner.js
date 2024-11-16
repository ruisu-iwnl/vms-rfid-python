let scanning = false;
let scanCount = 0;
const maxScans = 10; 
let shouldStopScanning = false;

function toggleScanning() {
    const rfidInput = document.getElementById('rfid-input');
    const scanButton = document.getElementById('scan_button');

    if (!scanning) {
        rfidInput.value = ''; 
        rfidInput.disabled = false; 
        rfidInput.focus(); 
        scanButton.textContent = 'Cancel Scanning'; 
        scanButton.classList.remove('bg-green-500');
        scanButton.classList.add('bg-red-500'); 
        scanning = true;
        scanCount = 0; 
        shouldStopScanning = false;

        rfidInput.addEventListener('input', updateDisplay);
        rfidInput.addEventListener('blur', function() {
            rfidInput.focus(); 
        });
        rfidInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                handleSubmit(event); // Submit the form when Enter is pressed
            }
        });

        console.log("Scanning started."); 
    } else {
        stopScanning();
    }
}

function stopScanning() {
    const rfidInput = document.getElementById('rfid-input');
    const scanButton = document.getElementById('scan_button');
    rfidInput.disabled = true;
    scanButton.textContent = 'Start Scanning'; 
    scanButton.classList.remove('bg-red-500');
    scanButton.classList.add('bg-green-500'); 
    scanning = false;
    shouldStopScanning = false; 
    scanCount = 0; 
    rfidInput.removeEventListener('input', updateDisplay);
    updateDisplay(); 

    console.log("Scanning stopped."); 
}

function updateDisplay() {
    const rfidInput = document.getElementById('rfid-input');
    const display = document.getElementById('rfid_number');

    console.log("Current RFID input value:", rfidInput.value);
    
    if (rfidInput.value && /^[0-9]+$/.test(rfidInput.value)) {
        if (rfidInput.value.length > scanCount) {
            scanCount++;
        }
        if (scanCount >= maxScans) {
            shouldStopScanning = true;
        }
    }
    
    display.textContent = rfidInput.value ? rfidInput.value : 'None';

    if (shouldStopScanning && scanning) {
        stopScanning();
        handleSubmit(); 
    }
}

function handleSubmit(event) {
    if (event) {
        event.preventDefault(); 
    }

    const rfidInput = document.getElementById('rfid-input');
    const form = document.forms[0];

    // Create a hidden input to store the detected plate number
    const hiddenPlateInput = document.createElement('input');
    hiddenPlateInput.type = 'hidden';
    hiddenPlateInput.name = 'detected_plate_number';
    hiddenPlateInput.value = detectedPlateNumber; // Set detected plate number value

    form.appendChild(hiddenPlateInput); // Append to form
    if (scanning) {
        stopScanning();
    }

    rfidInput.disabled = false;
    form.submit(); // Submit the form
}
