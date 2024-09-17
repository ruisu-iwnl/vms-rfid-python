document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('vehicleData');
    var labelsString = chartDataElement.getAttribute('data-labels');
    var dataString = chartDataElement.getAttribute('data-data');

    console.log('Vehicle Chart Labels:', labelsString);
    console.log('Vehicle Data:', dataString);

    // Parse labels and data from data attributes
    var dailyLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var dailyData = dataString ? dataString.split(',').map(Number) : [];

    console.log('Parsed Labels:', dailyLabels);
    console.log('Parsed Data:', dailyData);

    // Default to days of the week if no data is provided
    if (dailyLabels.length === 0) {
        dailyLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        dailyData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 20) + 1); // Random vehicle counts
    } else {
        // Append day of the week to each label
        dailyLabels = dailyLabels.map(label => {
            const date = new Date(label);
            const dayName = date.toLocaleDateString('en-US', { weekday: 'long' });
            return `${dayName} ${label}`;
        });
    }

    var ctx = document.getElementById('vehicleChart').getContext('2d');
    var vehicleChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dailyLabels,
            datasets: [{
                label: 'Number of Vehicles',
                data: dailyData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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
                            return context.label + ': ' + context.raw + ' vehicles';
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
                        maxTicksLimit: 7 // Limit number of labels shown
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
