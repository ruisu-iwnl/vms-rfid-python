let scanning = true;
let scanCount = 0;
const maxScans = 10;
let shouldStopScanning = false;
let lastKeyTime = Date.now();
const maxDelay = 20; 
const requiredLength = 10; 
let showDebugDisplay = false; 

document.addEventListener('DOMContentLoaded', function() {
    toggleScanning();
});

function toggleScanning() {
    const rfidInput = document.getElementById('rfid-input');
    const scanButton = document.getElementById('scan_button');

    if (!scanning) {
        stopScanning();
    } else {
        rfidInput.value = ''; 
        rfidInput.disabled = false; 
        rfidInput.focus(); 
        
        scanning = true;
        scanCount = 0; 
        shouldStopScanning = false;

        rfidInput.addEventListener('input', updateDisplay);
        rfidInput.addEventListener('blur', function() {
            rfidInput.focus(); 
        });

        rfidInput.addEventListener('keydown', function(event) {
            if (event.key !== 'Enter' && !/^[0-9]$/.test(event.key)) {
                event.preventDefault();
            }

            const currentTime = Date.now();
            const timeElapsed = currentTime - lastKeyTime;

            if (timeElapsed > maxDelay && rfidInput.value.length > 0) {
                rfidInput.value = rfidInput.value.slice(0, -1);

                if (showDebugDisplay) {
                    const display = document.getElementById('rfid_number');
                    display.textContent = '';  
                }
            }
            lastKeyTime = currentTime;
        });

        console.log("Scanning started.");
    }
}


function stopScanning() {
    const rfidInput = document.getElementById('rfid-input');
    const scanButton = document.getElementById('scan_button');
    rfidInput.disabled = true;
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

    if (rfidInput.value && /^[0-9]+$/.test(rfidInput.value)) {
        if (rfidInput.value.length > scanCount) {
            scanCount++;
        }
        if (scanCount >= maxScans) {
            shouldStopScanning = true;
        }
    }

    if (showDebugDisplay) {
        display.textContent = rfidInput.value ? rfidInput.value : 'None';
    }

    if (rfidInput.value.length === requiredLength && shouldStopScanning && scanning) {
        stopScanning();
        handleSubmit(); 
    }
}

function handleSubmit(event) {
    if (event) {
        event.preventDefault(); 
    }

    const rfidInput = document.getElementById('rfid-input');

    if (scanning) {
        stopScanning();
    }

    rfidInput.disabled = false;
    document.forms[0].submit();
}
