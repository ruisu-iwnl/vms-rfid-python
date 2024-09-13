document.addEventListener('DOMContentLoaded', function() {
    const rfidInput = document.getElementById('rfid-input');
    const rfidButton = document.getElementById('rfid-button');
    const statusMessage = document.getElementById('status-message');
    
    let debounceTimeout;
    const initialMessage = statusMessage.textContent;  
    const scanPromptMessage = 'TAP YOUR CARD ON THE RFID READER';  
    
    rfidInput.disabled = true;  

    rfidButton.addEventListener('click', function() {
        rfidInput.disabled = false; 
        rfidInput.focus();
        statusMessage.textContent = scanPromptMessage;  
    });

    rfidInput.addEventListener('input', function() {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            const rfidNumber = rfidInput.value.trim();

            if (rfidNumber) {
                fetch('/dashboard/timeinout/process_rfid', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') 
                    },
                    body: JSON.stringify({ rfid: rfidNumber })
                })
                .then(response => response.json())
                .then(data => {
                    statusMessage.textContent = `RFID SCANNED: ${data.rfid_number}`;
                    rfidInput.value = ''; 
                    rfidInput.disabled = true;  

                    setTimeout(() => {
                        statusMessage.textContent = initialMessage;
                    }, 5000); 
                })
                .catch(error => {
                    console.error('Error:', error);
                    statusMessage.textContent = 'An error occurred while processing the RFID.';
                });
            }
        }, 300); 
    });
});
