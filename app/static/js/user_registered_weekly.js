document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('userRegistrationData');
    var labelsString = chartDataElement.getAttribute('data-labels');
    var dataString = chartDataElement.getAttribute('data-data');

    console.log('User Registration Labels:', labelsString);
    console.log('User Registration Data:', dataString);

    // Parse labels and data from data attributes
    var registrationLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var registrationData = dataString ? dataString.split(',').map(Number) : [];

    console.log('Parsed Labels:', registrationLabels);
    console.log('Parsed Data:', registrationData);

    // Default to sample data if no data is provided
    if (registrationLabels.length === 0) {
        const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        registrationLabels = daysOfWeek;
        registrationData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 20) + 1); // Random user counts
    } else {
        // Append day of the week to each label
        registrationLabels = registrationLabels.map(label => {
            const date = new Date(label);
            const dayName = date.toLocaleDateString('en-US', { weekday: 'long' });
            return `${dayName} ${date.toLocaleDateString('en-US', { month: 'short' })} ${date.getDate()}`;
        });
    }

    var ctx = document.getElementById('userregistration').getContext('2d');
    var userRegistrationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: registrationLabels,
            datasets: [{
                label: 'Number of New Users',
                data: registrationData,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.raw + ' users';
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 30,
                        autoSkip: true,
                        maxTicksLimit: 7 // Show one label per day of the week
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
