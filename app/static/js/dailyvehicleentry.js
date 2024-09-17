document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('dailyVehicleEntriesData');
    var labelsString = chartDataElement.getAttribute('data-labels');
    var dataString = chartDataElement.getAttribute('data-data');

    console.log('Vehicle Entries Labels:', labelsString);
    console.log('Vehicle Entries Data:', dataString);

    // Parse labels and data from data attributes
    var entryLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var entryData = dataString ? dataString.split(',').map(Number) : [];

    console.log('Parsed Labels:', entryLabels);
    console.log('Parsed Data:', entryData);

    // Default to sample data if no data is provided
    if (entryLabels.length === 0) {
        const hoursOfDay = Array.from({ length: 24 }, (_, i) => `${i}:00 - ${i + 1}:00`);
        entryLabels = hoursOfDay;
        entryData = Array.from({ length: 24 }, () => Math.floor(Math.random() * 20) + 1); // Random vehicle counts
    } else {
        // Format labels as hourly intervals
        entryLabels = entryLabels.map(label => {
            const date = new Date(label);
            const hour = date.getHours();
            return `${hour}:00 - ${hour + 1}:00`;
        });
    }

    var ctx = document.getElementById('dailyVehicleEntriesChart').getContext('2d');
    var vehicleEntriesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: entryLabels,
            datasets: [{
                label: 'Number of Vehicle Entries',
                data: entryData,
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
                        maxTicksLimit: 24 // Show one label per hour of the day
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
