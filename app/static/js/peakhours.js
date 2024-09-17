document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('peakHoursData');
    var labelsString = chartDataElement.getAttribute('data-labels');
    var dataString = chartDataElement.getAttribute('data-data');

    console.log('Peak Hours Labels:', labelsString);
    console.log('Peak Hours Data:', dataString);

    // Parse labels and data from data attributes
    var peakHoursLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var peakHoursData = dataString ? dataString.split(',').map(Number) : [];

    console.log('Parsed Labels:', peakHoursLabels);
    console.log('Parsed Data:', peakHoursData);

    // Default to sample data if no data is provided
    if (peakHoursLabels.length === 0) {
        const hoursOfDay = Array.from({ length: 24 }, (_, i) => `${i}:00 - ${i + 1}:00`);
        peakHoursLabels = hoursOfDay;
        peakHoursData = Array.from({ length: 24 }, () => Math.floor(Math.random() * 20) + 1); // Random vehicle counts
    } else {
        // Format labels as hourly intervals
        peakHoursLabels = peakHoursLabels.map(label => {
            const date = new Date(label);
            const hour = date.getHours();
            return `${hour}:00 - ${hour + 1}:00`;
        });
    }

    var ctx = document.getElementById('peakHoursChart').getContext('2d');
    var peakHoursChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: peakHoursLabels,
            datasets: [{
                label: 'Number of Vehicle Entries',
                data: peakHoursData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: true // Fill the area under the line
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
