document.getElementById('toggle-orcr-blur').addEventListener('click', function() {
    var orcrImage = document.getElementById('orcr-image');
    var icon = this;

    orcrImage.classList.toggle('blur-lg');
    
    if (orcrImage.classList.contains('blur-lg')) {
        icon.textContent = '👁️';
    } else {
        icon.textContent = '👁️‍🗨️';
    }
});

document.getElementById('toggle-driver-license-blur').addEventListener('click', function() {
    var driverLicenseImage = document.getElementById('driver-license-image');
    var icon = this;

    driverLicenseImage.classList.toggle('blur-lg');
    
    if (driverLicenseImage.classList.contains('blur-lg')) {
        icon.textContent = '👁️';
    } else {
        icon.textContent = '👁️‍🗨️';
    }
});

document.getElementById('edit-button').addEventListener('click', () => {
    document.querySelectorAll('input').forEach(input => {
        input.classList.remove('hidden');
        input.classList.add('opacity-100');
    });

    document.querySelectorAll('span[id$="-text"]').forEach(span => {
        span.classList.add('opacity-0');
        setTimeout(() => span.classList.add('hidden'), 300); 
    });

    document.getElementById('file-inputs').classList.remove('hidden');
    
    document.getElementById('edit-button').classList.add('hidden');
    document.getElementById('save-button').classList.remove('hidden');
    document.getElementById('cancel-button').classList.remove('hidden');

    document.getElementById('orcr-image').classList.remove('blur-lg');
    document.getElementById('driver-license-image').classList.remove('blur-lg');

    document.getElementById('toggle-orcr-blur').textContent = '👁️‍🗨️';
    document.getElementById('toggle-driver-license-blur').textContent = '👁️‍🗨️';

    document.getElementById('edit-orcr-icon').classList.remove('hidden');
    document.getElementById('edit-driver-license-icon').classList.remove('hidden');

    document.getElementById('profile-image-input').classList.remove('hidden');
    document.getElementById('orcr-image-input').classList.remove('hidden');
    document.getElementById('driver-license-image-input').classList.remove('hidden');
});

document.getElementById('cancel-button').addEventListener('click', () => {
    location.reload();
});
