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
    shouldStopScanning = false; // Reset this flag
    scanCount = 0; // Reset scanCount as well
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

    // Check if we need to stop scanning and submit the form
    if (shouldStopScanning && scanning) {
        stopScanning();
        handleSubmit(); // Submit the form when maximum scans reached
    }
}

function handleSubmit(event) {
    if (event) {
        event.preventDefault(); // Prevent default form submission
    }

    const rfidInput = document.getElementById('rfid-input');

    // Enable the input to ensure it's submitted
    if (scanning) {
        stopScanning();
    }

    // Ensure the input is ready for submission
    rfidInput.disabled = false;

    // Submit the form
    document.forms[0].submit(); // Submit the form
}