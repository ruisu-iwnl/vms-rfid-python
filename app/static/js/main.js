// date and time
// call out 'date' and 'time'
document.addEventListener('DOMContentLoaded', function() {
    function updateDateTime() {
        const now = new Date();
        const dateOptions = {
            year: 'numeric',
            month: 'long',
            day: '2-digit'
        };
        const timeOptions = {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        };
        const dateString = now.toLocaleDateString('en-US', dateOptions);
        const timeString = now.toLocaleTimeString('en-US', timeOptions);

        const dateElement = document.getElementById('date');
        const timeElement = document.getElementById('time');

        if (dateElement) {
            dateElement.textContent = dateString;
        }
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }

    updateDateTime();
    setInterval(updateDateTime, 1000);
});
